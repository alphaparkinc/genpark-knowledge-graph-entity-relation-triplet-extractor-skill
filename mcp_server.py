import sys, json
from client import KnowledgeGraphTripletExtractor

def main():
    engine = KnowledgeGraphTripletExtractor()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            rid = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "extract_from_text", "description": "Extract triplets.", "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}},
                        {"name": "find_shortest_path", "description": "Find path.", "inputSchema": {"type": "object", "properties": {"start": {"type": "string"}, "target": {"type": "string"}}, "required": ["start", "target"]}},
                        {"name": "export_cypher", "description": "Export Cypher.", "inputSchema": {"type": "object"}},
                        {"name": "run_benchmark_graph_extractor", "description": "Run self-test.", "inputSchema": {"type": "object"}}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "extract_from_text":
                    out = engine.extract_from_text(args.get("text", ""))
                elif tname == "find_shortest_path":
                    out = engine.find_shortest_path(args.get("start", ""), args.get("target", ""))
                elif tname == "export_cypher":
                    out = engine.export_cypher()
                elif tname == "run_benchmark_graph_extractor":
                    out = engine.run_benchmark_graph_extractor()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
