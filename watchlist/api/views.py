from watchlist.models import Movie
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from watchlist.api.serializers import MovieSerializer

class MovieList(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        data = MovieSerializer(movies, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MovieSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "valid",
                "message": "Movie created successfully",
                "data": serializer.data
            }
            return Response(data, status=201)
        else:
            return Response(serializer.data, status=404)
        

class MovieDetails(APIView):
    def get(self, request, id):
        try:
            movie = Movie.objects.get(pk=id)
        except Movie.DoesNotExist:
            res_data = {'status':'invalid', 'message':'movie not found'}
            return Response(res_data, status=status.HTTP_404_NOT_FOUND)
        data = MovieSerializer(movie).data
        return Response(data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        movie = Movie.objects.get(pk=id)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()
        data = {
            "status": "valid",
            "message": "Movie deleted successfully",
        }
        return Response(data, status=204)

# @api_view(['GET'])
# def movies_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         data = MovieSerializer(movies, many=True).data
#         return Response(data, status=status.HTTP_200_OK)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, id):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=id)
#         except Movie.DoesNotExist:
#             res_data = {'status':'invalid', 'message':'movie not found'}
#             return Response(res_data, status=status.HTTP_404_NOT_FOUND)
#         data = MovieSerializer(movie).data
#         return Response(data, status=status.HTTP_200_OK)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=id)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=id)
#         movie.delete()
#         data = {
#             "status": "valid",
#             "message": "Movie deleted successfully",
#         }
#         return Response(data, status=204)

# @api_view(['POST'])
# def movies_create(request):
#     serializer = MovieSerializer(data = request.data)
#     if serializer.is_valid():
#         serializer.save()
#         data = {
#             "status": "valid",
#             "message": "Movie created successfully",
#             "data": serializer.data
#         }
#         return Response(data, status=201)
#     else:
#         return Response(serializer.data, status=404)
    

# serializer = MovieSerializer(data = request.data)
# if serializer.is_valid():
#     serializer.save()
#     return Response(serializer.data, status=201)
# else :
#     return Response(serializer.errors, status=404)
