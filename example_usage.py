from client import KnowledgeGraphTripletExtractor
import json

def main():
    engine = KnowledgeGraphTripletExtractor()
    res = engine.run_benchmark_graph_extractor()
    print("Knowledge Graph Triplet Extractor Benchmark Result:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
