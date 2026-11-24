'use client';

import React, { useEffect, useState, useMemo, useCallback } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  MarkerType,
  Handle,
  Position,
  NodeProps
} from 'reactflow';
import 'reactflow/dist/style.css';
import {
  Search,
  Filter,
  Maximize2,
  RefreshCw,
  AlertTriangle,
  Info,
  ShieldAlert,
  ArrowRight,
  X,
  CreditCard,
  Building,
  User,
  CheckCircle2,
  Layers
} from 'lucide-react';
import { fetchGraph } from '@/lib/api';

// Custom Account Node for React Flow
function AccountNode({ data, selected }: NodeProps) {
  const isMule = data.is_mule_candidate;
  const isHighRisk = data.risk_level === 'CRITICAL' || data.risk_level === 'HIGH';

  return (
    <div
      className={`w-64 bg-white rounded-lg border-2 shadow-md transition-all select-none font-sans text-xs overflow-hidden ${
        selected
          ? 'border-sky-600 ring-2 ring-sky-300'
          : isMule
          ? 'border-rose-500'
          : isHighRisk
          ? 'border-amber-400'
          : 'border-slate-300'
      }`}
    >
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-slate-400" />

      {/* Node Header */}
      <div
        className={`px-3 py-1.5 flex items-center justify-between text-[11px] font-semibold text-white ${
          isMule
            ? 'bg-rose-700'
            : isHighRisk
            ? 'bg-amber-700'
            : 'bg-tg-sidebar'
        }`}
      >
        <span className="truncate max-w-[130px]">{data.bank_name || 'Bank Account'}</span>
        <span className="px-1 py-0.2 rounded text-[9px] uppercase font-mono bg-black/30 text-white font-bold">
          {data.risk_level}
        </span>
      </div>

      {/* Node Body */}
      <div className="p-3 space-y-1.5 bg-white">
        <div className="flex items-center justify-between">
          <span className="font-mono text-xs font-bold text-slate-800 truncate">
            {data.account_number}
          </span>
          {isMule && (
            <span className="bg-rose-100 text-rose-700 border border-rose-300 text-[9px] px-1 rounded font-bold uppercase">
              Mule
            </span>
          )}
        </div>

        <p className="text-[11px] text-slate-600 font-medium truncate">
          {data.account_holder}
        </p>

        {/* Ledger Inflow/Outflow stats */}
        <div className="grid grid-cols-2 gap-1 pt-1.5 border-t border-slate-100 text-[10px] font-mono">
          <div>
            <span className="text-slate-400 block text-[9px]">INFLOW</span>
            <span className="text-emerald-700 font-semibold truncate block">
              ₹{(data.inflow || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block text-[9px]">OUTFLOW</span>
            <span className="text-rose-700 font-semibold truncate block">
              ₹{(data.outflow || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
            </span>
          </div>
        </div>

        {/* Degrees */}
        <div className="flex items-center justify-between pt-1 text-[10px] text-slate-400 border-t border-slate-50">
          <span>In-Hops: {data.in_degree}</span>
          <span>Out-Hops: {data.out_degree}</span>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-slate-400" />
    </div>
  );
}

interface NetworkGraphViewProps {
  selectedCaseId: string;
}

export default function NetworkGraphView({ selectedCaseId }: NetworkGraphViewProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters & selection
  const [minAmount, setMinAmount] = useState<number>(0);
  const [searchAccount, setSearchAccount] = useState<string>('');
  const [selectedNodeData, setSelectedNodeData] = useState<any | null>(null);
  const [selectedEdgeData, setSelectedEdgeData] = useState<any | null>(null);

  const nodeTypes = useMemo(() => ({ accountNode: AccountNode }), []);

  const loadGraph = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchGraph(selectedCaseId, minAmount);
      // Map edges to styled React Flow edges
      const styledEdges = data.edges.map((e: any) => {
        const amt = e.data.total_amount;
        const isSusp = e.data.has_suspicious;
        return {
          ...e,
          label: `₹${amt.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`,
          labelStyle: { fill: isSusp ? '#BD4A4A' : '#172333', fontWeight: 600, fontSize: 10, fontFamily: 'monospace' },
          labelBgStyle: { fill: '#FFFFFF', fillOpacity: 0.95, stroke: isSusp ? '#BD4A4A' : '#DCE2E8', strokeWidth: 1 },
          labelBgPadding: [4, 2],
          labelBgBorderRadius: 4,
          style: {
            stroke: isSusp ? '#BD4A4A' : '#64748B',
            strokeWidth: isSusp ? 2.5 : 1.5,
          },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: isSusp ? '#BD4A4A' : '#64748B',
            width: 14,
            height: 14,
          },
        };
      });

      setNodes(data.nodes);
      setEdges(styledEdges);
      setSummary(data.summary);
    } catch (err: any) {
      setError(err.message || 'Failed to construct graph');
    } finally {
      setLoading(false);
    }
  }, [selectedCaseId, minAmount, setNodes, setEdges]);

  useEffect(() => {
    loadGraph();
  }, [loadGraph]);

  const onNodeClick = (_: any, node: any) => {
    setSelectedNodeData(node.data);
    setSelectedEdgeData(null);
  };

  const onEdgeClick = (_: any, edge: any) => {
    setSelectedEdgeData(edge.data);
    setSelectedNodeData(null);
  };

  // Search filter
  const handleSearchAccount = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchAccount.trim()) return;
    const target = nodes.find(
      (n) =>
        n.id.toLowerCase().includes(searchAccount.toLowerCase()) ||
        n.data.account_holder.toLowerCase().includes(searchAccount.toLowerCase())
    );
    if (target) {
      setSelectedNodeData(target.data);
      setSelectedEdgeData(null);
    } else {
      alert(`Account "${searchAccount}" not found in current case graph.`);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full relative overflow-hidden bg-slate-50">
      {/* Top Filter and Search Toolbar */}
      <div className="bg-white border-b border-tg-border px-5 py-2.5 flex flex-wrap items-center justify-between gap-3 z-10 shadow-sm">
        <form onSubmit={handleSearchAccount} className="flex items-center space-x-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
            <input
              type="text"
              placeholder="Locate Account Number / Holder..."
              value={searchAccount}
              onChange={(e) => setSearchAccount(e.target.value)}
              className="pl-8 pr-3 py-1.5 text-xs rounded border border-slate-300 w-64 focus:outline-none focus:border-tg-primary font-mono"
            />
          </div>
          <button
            type="submit"
            className="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs rounded border border-slate-300 font-medium"
          >
            Find Node
          </button>
        </form>

        {/* Threshold Slider */}
        <div className="flex items-center space-x-3 text-xs">
          <span className="font-semibold text-slate-700">Min Amount Filter:</span>
          <input
            type="range"
            min="0"
            max="1000000"
            step="25000"
            value={minAmount}
            onChange={(e) => setMinAmount(Number(e.target.value))}
            className="w-32 accent-tg-primary cursor-pointer"
          />
          <span className="font-mono text-slate-600 font-bold min-w-[70px]">
            {minAmount === 0 ? 'All Flow' : `≥ ₹${(minAmount / 1000).toFixed(0)}k`}
          </span>

          <button
            onClick={() => loadGraph()}
            className="px-2.5 py-1 text-xs bg-tg-primary text-white rounded hover:bg-tg-primaryHover flex items-center space-x-1"
          >
            <RefreshCw className="w-3 h-3" />
            <span>Redraw Graph</span>
          </button>
        </div>

        {/* Graph Topological Stats Pill */}
        {summary && (
          <div className="hidden xl:flex items-center space-x-2 text-[11px] font-mono text-slate-600 bg-slate-50 px-2.5 py-1 rounded border border-slate-200">
            <span>Nodes: <strong>{summary.total_nodes}</strong></span>
            <span>&bull;</span>
            <span>Edges: <strong>{summary.total_edges}</strong></span>
            <span>&bull;</span>
            <span className="text-rose-700">Mules: <strong>{summary.mule_conduits_count}</strong></span>
          </div>
        )}
      </div>

      {/* Main Canvas Area */}
      <div className="flex-1 relative h-full">
        {loading ? (
          <div className="absolute inset-0 bg-white/70 backdrop-blur-xs flex items-center justify-center z-20">
            <div className="flex items-center space-x-2 text-slate-600 text-xs font-medium">
              <RefreshCw className="w-4 h-4 animate-spin text-tg-primary" />
              <span>Synthesizing NetworkX directed graph topology...</span>
            </div>
          </div>
        ) : error ? (
          <div className="p-8 text-center text-rose-600 text-xs">
            {error}
          </div>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            onEdgeClick={onEdgeClick}
            fitView
            fitViewOptions={{ padding: 0.2 }}
            minZoom={0.2}
            maxZoom={2.0}
            attributionPosition="bottom-right"
          >
            <Background color="#CBD5E1" gap={20} size={1} />
            <Controls />
            <MiniMap
              nodeColor={(n: any) =>
                n.data?.is_mule_candidate ? '#BD4A4A' : n.data?.risk_level === 'CRITICAL' ? '#D69A36' : '#245B88'
              }
              className="bg-white border border-slate-300 rounded shadow-sm"
            />
          </ReactFlow>
        )}

        {/* Side Inspector Drawer: Account Node Selected */}
        {selectedNodeData && (
          <div className="absolute top-4 right-4 w-80 bg-white border border-tg-border rounded-lg shadow-xl p-4 z-30 max-h-[90%] overflow-y-auto text-xs space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <Building className="w-4 h-4 text-tg-primary" />
                <h3 className="font-bold text-sm text-tg-text">Target Account Profile</h3>
              </div>
              <button
                onClick={() => setSelectedNodeData(null)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div>
              <span className="text-[10px] text-slate-400 uppercase font-semibold block">
                Account Number
              </span>
              <span className="font-mono text-sm font-bold text-slate-900 block">
                {selectedNodeData.account_number}
              </span>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-500">Holder:</span>
                <span className="font-semibold text-slate-800">{selectedNodeData.account_holder}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Bank:</span>
                <span className="font-semibold text-slate-800">{selectedNodeData.bank_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Type:</span>
                <span className="font-mono text-slate-800">{selectedNodeData.account_type}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Risk Level:</span>
                <span className="font-bold text-rose-700 uppercase">{selectedNodeData.risk_level}</span>
              </div>
            </div>

            {/* Financial Throughput */}
            <div className="bg-slate-50 p-2.5 rounded border border-slate-200 font-mono space-y-1">
              <div className="flex justify-between text-emerald-700">
                <span>Total Inflow:</span>
                <span>₹{(selectedNodeData.inflow || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</span>
              </div>
              <div className="flex justify-between text-rose-700">
                <span>Total Outflow:</span>
                <span>₹{(selectedNodeData.outflow || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</span>
              </div>
              <div className="flex justify-between text-slate-700 pt-1 border-t border-slate-200 text-[10px]">
                <span>Degree Centrality:</span>
                <span>In: {selectedNodeData.in_degree} &bull; Out: {selectedNodeData.out_degree}</span>
              </div>
            </div>

            {/* Risk Tags */}
            {selectedNodeData.risk_tags && selectedNodeData.risk_tags.length > 0 && (
              <div>
                <span className="text-[10px] text-slate-400 uppercase font-semibold block mb-1">
                  Forensic Indicators
                </span>
                <div className="flex flex-wrap gap-1">
                  {selectedNodeData.risk_tags.map((t: string, i: number) => (
                    <span
                      key={i}
                      className="bg-rose-50 text-rose-700 border border-rose-200 px-1.5 py-0.5 rounded text-[10px] font-mono font-medium"
                    >
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Recommended Legal Notice */}
            <div className="p-2.5 bg-amber-50 border border-amber-200 rounded text-[11px] text-amber-900 space-y-1">
              <span className="font-bold block">Recommended Investigative Action:</span>
              <p>
                Issue Section 91 CrPC notice to <strong>{selectedNodeData.bank_name}</strong> for certified Account Opening Form (AOF), KYC biometric records, and IP access logs.
              </p>
            </div>
          </div>
        )}

        {/* Side Inspector Drawer: Edge Selected */}
        {selectedEdgeData && (
          <div className="absolute top-4 right-4 w-80 bg-white border border-tg-border rounded-lg shadow-xl p-4 z-30 max-h-[90%] overflow-y-auto text-xs space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <CreditCard className="w-4 h-4 text-tg-primary" />
                <h3 className="font-bold text-sm text-tg-text">Directed Transaction Edge</h3>
              </div>
              <button
                onClick={() => setSelectedEdgeData(null)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="bg-slate-50 p-2.5 rounded border border-slate-200 font-mono space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-500">Total Transferred:</span>
                <span className="font-bold text-tg-critical text-sm">
                  ₹{selectedEdgeData.total_amount?.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                </span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>Transaction Count:</span>
                <span>{selectedEdgeData.transaction_count} transaction(s)</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>Transfer Mode:</span>
                <span>{selectedEdgeData.transaction_type}</span>
              </div>
            </div>

            {/* Transactions List along this edge */}
            {selectedEdgeData.transactions && selectedEdgeData.transactions.length > 0 && (
              <div>
                <span className="text-[10px] text-slate-400 uppercase font-semibold block mb-1">
                  Underlying Transactions ({selectedEdgeData.transactions.length})
                </span>
                <div className="space-y-1.5 max-h-48 overflow-y-auto">
                  {selectedEdgeData.transactions.map((tx: any, idx: number) => (
                    <div key={idx} className="p-2 bg-slate-50 border border-slate-200 rounded font-mono text-[11px]">
                      <div className="flex justify-between font-semibold text-slate-800">
                        <span>{tx.id}</span>
                        <span>₹{Number(tx.amount).toLocaleString('en-IN')}</span>
                      </div>
                      <div className="text-[10px] text-slate-500">
                        {tx.timestamp ? new Date(tx.timestamp).toLocaleString('en-GB') : 'Recorded Tx'}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

