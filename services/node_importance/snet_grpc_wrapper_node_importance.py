import grpc
from concurrent import futures
import time
import logging

from service_spec_node_importance import node_importance_pb2
from service_spec_node_importance import node_importance_pb2_grpc

from node_importance import NodeImportance


class NodeImportanceServicer(node_importance_pb2_grpc.NodeImportanceServicer):
    def CentralNodes(self, request, context):
        ni = NodeImportance()
        graph = request.graph
        usebounds = request.usebounds

        try:
            edges_list = []
            for edges_proto in graph.edges:
                edges_list.append(list(edges_proto.edge))

            graph_in = {"nodes": list(graph.nodes), "edges": edges_list}

            temp_response = ni.find_central_nodes(graph=graph_in, usebounds=usebounds)

            if temp_response[0]:


                response = node_importance_pb2.CentralNodeResponse(status=temp_response[0], message=temp_response[1], output=temp_response[2])
                return response

            else:
                print(time.strftime("%c"))
                print('Waiting for next call on port 5002.')

                raise grpc.RpcError(grpc.StatusCode.UNKNOWN, temp_response[1])


        except Exception as e:

            logging.exception("message")

            print(time.strftime("%c"))
            print('Waiting for next call on port 5002.')

            raise grpc.RpcError(grpc.StatusCode.UNKNOWN, str(e))


    def Periphery(self, request, context):
        ni = NodeImportance()
        graph = request.graph
        usebounds = request.usebounds

        try:
            edges_list = []
            for edges_proto in graph.edges:
                edges_list.append(list(edges_proto.edge))

            graph_in = {"nodes": list(graph.nodes), "edges": edges_list}

            temp_response = ni.find_Periphery(graph=graph_in, usebounds=usebounds)

            if temp_response[0]:

                response = node_importance_pb2.PeripheryResponse(status=temp_response[0], message=temp_response[1],
                                                                   output=temp_response[2])
                return response

            else:
                print(time.strftime("%c"))
                print('Waiting for next call on port 5002.')

                raise grpc.RpcError(grpc.StatusCode.UNKNOWN, temp_response[1])


        except Exception as e:

            logging.exception("message")

            print(time.strftime("%c"))
            print('Waiting for next call on port 5002.')

            raise grpc.RpcError(grpc.StatusCode.UNKNOWN, str(e))

    def ClosenessCentrality(self, request, context):
        ni = NodeImportance()
        graph = request.graph
        distance = request.distance
        wf_improved = request.wf_improved
        reverse = request.reverse
        directed = request.directed


        try:
            edges_list = []
            for edges_proto in graph.edges:
                edges_list.append(list(edges_proto.edge))

            weights_list = list(graph.weights)

            nodes_list = list(graph.nodes)


            if len(weights_list) > 0:
                graph_in = {"nodes": nodes_list, "edges": edges_list, "weights": weights_list}
            else:
                graph_in = {"nodes": nodes_list, "edges": edges_list}

            ret = ni.find_closeness_centrality(graph_in, distance = distance, wf_improved = wf_improved, reverse = reverse, directed = directed)

            resp = node_importance_pb2.ClosenessCentralityResponse(status=ret[0], message=ret[1])


            if resp.status:
                dict_resp = []
                for node_ele,val_ele in (ret[2]["closeness_centrality"]).items():
                    dict_resp.append(node_importance_pb2.DictOutput(node=node_ele, output=val_ele))

                resp = node_importance_pb2.ClosenessCentralityResponse(status=ret[0], message=ret[1], output=dict_resp)

            else:

                print(time.strftime("%c"))
                print('Waiting for next call on port 5000.')

                raise grpc.RpcError(grpc.StatusCode.UNKNOWN, ret[1])

            print('status:',resp.status)
            print('message:',resp.message)
            print(time.strftime("%c"))
            print('Waiting for next call on port 5000.')

            return resp


        except Exception as e:

            logging.exception("message")

            print(time.strftime("%c"))
            print('Waiting for next call on port 5000.')

            raise grpc.RpcError(grpc.StatusCode.UNKNOWN, str(e))



    def DegreeCentrality(self, request, context):
        ni = NodeImportance()
        graph = request.graph

        try:
            edges_list = []
            weights_list = []
            for edges_proto in graph.edges:
                edges_list.append(list(edges_proto.edge))
            if len(graph.weights) > 0:
                for weights_proto in graph.weights:
                    weights_list.append(int(weights_proto))
            graph_in = {"nodes": list(graph.nodes), "edges": edges_list, "weights": weights_list}
        except Exception as e:
            return [False, str(e), {}]

        temp_response = ni.find_degree_centrality(graph_in, request.in_out)
        centrality_output_edges = []
        centrality_output_value = []
        if temp_response[0]:
            for k, v in temp_response[2][str(request.in_out) + "degree_centrality"].items():
                centrality_output_edges.append(k)
                centrality_output_value.append(v)

        output = node_importance_pb2.DictOutput(node=centrality_output_edges,
                                                output=centrality_output_value)
        response = node_importance_pb2.DegreeCentralityResponse(status=temp_response[0], message=temp_response[1],
                                                                output=output)
        return response

    def BetweennessCentrality(self, request, context):
        ni = NodeImportance()
        graph = request.graph

        try:
            edges_list = []
            for edges_proto in graph.edges:
                edges_list.append(list(edges_proto.edge))

            weights_list = list(graph.weights)

            nodes_list = list(graph.nodes)

            if len(weights_list) > 0:
                graph_in = {"nodes": nodes_list, "edges": edges_list, "weights": weights_list}
            else:
                graph_in = {"nodes": nodes_list, "edges": edges_list}

            ret = ni.find_betweenness_centrality(graph_in, k=request.k, normalized=request.normalized,
                                           weight=request.weight, endpoints=request.endpoints,
                                           type=request.type, seed=request.seed, directed=request.directed)

            if ret[0]:
                dict_resp = []
                if ret[2]['type'] == 'node':
                    for node_ele, val_ele in (ret[2]["betweenness_centrality"]).items():
                        dict_resp.append(node_importance_pb2.DictOutput(node=node_ele, output=val_ele))
                else:
                    for edge_ele, val_ele in (ret[2]["betweenness_centrality"]).items():
                        edges_resp = node_importance_pb2.Edge(edge=list(edge_ele))
                        dict_resp.append(node_importance_pb2.DictOutput(edge=edges_resp, output=val_ele))


                resp = node_importance_pb2.BetweennessCentralityResponse(status=ret[0], message=ret[1], output=dict_resp)

            else:

                print(time.strftime("%c"))
                print('Waiting for next call on port 5000.')

                raise grpc.RpcError(grpc.StatusCode.UNKNOWN, ret[1])

            print('status:', resp.status)
            print('message:', resp.message)
            print(time.strftime("%c"))
            print('Waiting for next call on port 5000.')

            return resp


        except Exception as e:

            logging.exception("message")

            print(time.strftime("%c"))

            print('Waiting for next call on port 5000.')

            raise grpc.RpcError(grpc.StatusCode.UNKNOWN, str(e))

    def PageRank(self, request, context):
        ni = NodeImportance()
        graph = request.graph

        try:
            edges_list = []
            weights_list = []
            for edges_proto in graph.edges:
                edges_list.append(list(edges_proto.edge))
            if len(graph.weights) > 0:
                for weights_proto in graph.weights:
                    weights_list.append(int(weights_proto))
            graph_in = {"nodes": list(graph.nodes), "edges": edges_list, "weights": weights_list}
        except Exception as e:
            return [False, str(e), {}]

        temp_response = ni.find_pagerank(graph_in, request.alpha, request.personalization, request.max_iter,
                                         request.tol, request.nstart, request.weight, request.dangling)
        pagerank_output_edges = []
        pagerank_output_value = []
        if temp_response[0]:
            for k, v in temp_response[2]["pagerank"].items():
                pagerank_output_edges.append(k)
                pagerank_output_value.append(v)

        output = node_importance_pb2.DictOutput(node=pagerank_output_edges,
                                                output=pagerank_output_value)
        response = node_importance_pb2.PageRankResponse(status=temp_response[0], message=temp_response[1],
                                                        output=output)
        return response

    def EigenvectorCentrality(self, request, context):
        ni = NodeImportance()
        graph = request.graph

        try:
            edges_list = []
            weights_list = []
            for edges_proto in graph.edges:
                edges_list.append(list(edges_proto.edge))
            if len(graph.weights) > 0:
                for weights_proto in graph.weights:
                    weights_list.append(int(weights_proto))
            graph_in = {"nodes": list(graph.nodes), "edges": edges_list, "weights": weights_list}
        except Exception as e:
            return [False, str(e), {}]

        temp_response = ni.find_eigenvector_centrality(graph_in, request.max_iter, request.tol, request.nstart,
                                                       request.weight)
        eigenvector_output_edges = []
        eigenvector_output_value = []
        if temp_response[0]:
            for k, v in temp_response[2]["eigenvector_centrality"].items():
                eigenvector_output_edges.append(k)
                eigenvector_output_value.append(v)

        output = node_importance_pb2.DictOutput(node=eigenvector_output_edges,
                                                output=eigenvector_output_value)

        response = node_importance_pb2.EigenvectorCentralityResponse(status=temp_response[0], message=temp_response[1],
                                                                     output=output)

        return response

    def Hits(self, request, context):
        ni = NodeImportance()
        graph = request.graph

        try:
            edges_list = []
            weights_list = []
            for edges_proto in graph.edges:
                edges_list.append(list(edges_proto.edge))
            if len(graph.weights) > 0:
                for weights_proto in graph.weights:
                    weights_list.append(int(weights_proto))
            graph_in = {"nodes": list(graph.nodes), "edges": edges_list, "weights": weights_list}
        except Exception as e:
            return [False, str(e), {}]

        temp_response = ni.find_hits(graph_in, request.nodelist, request.mode)
        hits_list = []
        if temp_response[0]:
            for i in temp_response[2][request.mode]:
                hits_list.append(node_importance_pb2.HitsOutput(hits_out=list(i)))

        response = node_importance_pb2.HitsResponse(status=temp_response[0], message=temp_response[1],
                                                    output=hits_list)

        return response


class Server():
    def __init__(self):
        self.port = '[::]:5002'
        self.server = None

    def start_server(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_importance_pb2_grpc.add_NodeImportanceServicer_to_server(NodeImportanceServicer(), self.server)
        print('Starting server. Listening on port 5002.')
        self.server.add_insecure_port(self.port)
        self.server.start()

    def stop_server(self):
        self.server.stop(0)