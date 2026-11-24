import networkx as nx
from typing import List, Dict, Any, Optional

class NetworkGraphService:
    """
    Transforms transaction records into NetworkX graph and exports
    clean, positioned nodes and edges tailored for React Flow.
    """

    @staticmethod
    def build_graph(
        transactions: List[Dict[str, Any]],
        accounts_map: Optional[Dict[str, Dict[str, Any]]] = None,
        min_amount: float = 0.0
    ) -> Dict[str, Any]:
        if accounts_map is None:
            accounts_map = {}

        filtered_tx = [t for t in transactions if float(t.get("amount", 0)) >= min_amount]

        G = nx.DiGraph()

        # Add edges and accumulate flow
        edge_data_map = {}
        for tx in filtered_tx:
            src = str(tx["sender_account"])
            dst = str(tx["receiver_account"])
            amt = float(tx.get("amount", 0))

            if not G.has_node(src):
                G.add_node(src)
            if not G.has_node(dst):
                G.add_node(dst)

            key = (src, dst)
            if key not in edge_data_map:
                edge_data_map[key] = {
                    "count": 0,
                    "total_amount": 0.0,
                    "transactions": [],
                    "has_suspicious": False
                }

            edge_data_map[key]["count"] += 1
            edge_data_map[key]["total_amount"] += amt
            edge_data_map[key]["transactions"].append(tx)
            if tx.get("risk_flag") not in ("NORMAL", None):
                edge_data_map[key]["has_suspicious"] = True

            if G.has_edge(src, dst):
                G[src][dst]["weight"] += amt
            else:
                G.add_edge(src, dst, weight=amt)

        # Compute graph metrics
        in_degrees = dict(G.in_degree())
        out_degrees = dict(G.out_degree())
        
        # Spring layout for 2D positioning
        pos = {}
        if len(G.nodes) > 0:
            try:
                # Use spring layout with k scaling
                raw_pos = nx.spring_layout(G, k=1.8, iterations=60, seed=42)
                # Scale positions to canvas coordinates (e.g. 100 to 1200 x, 100 to 700 y)
                for node, (px, py) in raw_pos.items():
                    pos[node] = {
                        "x": round((px + 1.2) * 450 + 80),
                        "y": round((py + 1.2) * 300 + 80)
                    }
            except Exception:
                # Fallback grid layout
                idx = 0
                for node in G.nodes:
                    pos[node] = {
                        "x": 150 + (idx % 5) * 220,
                        "y": 100 + (idx // 5) * 160
                    }
                    idx += 1

        # React Flow Nodes
        react_nodes = []
        for node_id in G.nodes:
            in_deg = in_degrees.get(node_id, 0)
            out_deg = out_degrees.get(node_id, 0)
            
            # Retrieve account metadata if available
            acc_info = accounts_map.get(node_id, {})
            holder = acc_info.get("account_holder", f"Account {node_id[-6:]}")
            bank = acc_info.get("bank_name", "Scheduled Commercial Bank")
            risk_level = acc_info.get("risk_level", "LOW")
            risk_score = acc_info.get("risk_score", 15.0)
            risk_tags = acc_info.get("risk_tags", [])
            if isinstance(risk_tags, str):
                import json
                try:
                    risk_tags = json.loads(risk_tags)
                except Exception:
                    risk_tags = []

            # Flag potential role
            is_mule = False
            if in_deg >= 2 and out_deg >= 2:
                is_mule = True
                if "MULE_CONDUIT" not in risk_tags:
                    risk_tags.append("MULE_CONDUIT")
                if risk_level in ("LOW", "MEDIUM"):
                    risk_level = "HIGH"

            node_position = pos.get(node_id, {"x": 200, "y": 200})

            react_nodes.append({
                "id": node_id,
                "type": "accountNode",
                "position": node_position,
                "data": {
                    "account_number": node_id,
                    "account_holder": holder,
                    "bank_name": bank,
                    "in_degree": in_deg,
                    "out_degree": out_deg,
                    "total_degree": in_deg + out_deg,
                    "risk_level": risk_level,
                    "risk_score": risk_score,
                    "risk_tags": risk_tags,
                    "is_mule_candidate": is_mule,
                    "inflow": acc_info.get("total_inflow", 0.0),
                    "outflow": acc_info.get("total_outflow", 0.0),
                    "account_type": acc_info.get("account_type", "SAVINGS")
                }
            })

        # React Flow Edges
        react_edges = []
        edge_index = 0
        for (src, dst), data in edge_data_map.items():
            edge_index += 1
            has_susp = data["has_suspicious"]
            latest_tx = data["transactions"][-1]
            
            react_edges.append({
                "id": f"edge-{src}-{dst}-{edge_index}",
                "source": src,
                "target": dst,
                "animated": has_susp,
                "type": "transactionEdge",
                "data": {
                    "total_amount": round(data["total_amount"], 2),
                    "transaction_count": data["count"],
                    "has_suspicious": has_susp,
                    "last_timestamp": str(latest_tx.get("timestamp", "")),
                    "transaction_type": latest_tx.get("transaction_type", "IMPS"),
                    "risk_flag": latest_tx.get("risk_flag", "NORMAL"),
                    "transactions": data["transactions"]
                }
            })

        # Calculate high level topology
        strongly_connected = list(nx.strongly_connected_components(G)) if len(G.nodes) > 0 else []
        weakly_connected = list(nx.weakly_connected_components(G)) if len(G.nodes) > 0 else []

        summary = {
            "total_nodes": len(react_nodes),
            "total_edges": len(react_edges),
            "weakly_connected_components": len(weakly_connected),
            "strongly_connected_components": len(strongly_connected),
            "high_risk_nodes_count": len([n for n in react_nodes if n["data"]["risk_level"] in ("HIGH", "CRITICAL")]),
            "mule_conduits_count": len([n for n in react_nodes if n["data"]["is_mule_candidate"]])
        }

        return {
            "nodes": react_nodes,
            "edges": react_edges,
            "summary": summary
        }

