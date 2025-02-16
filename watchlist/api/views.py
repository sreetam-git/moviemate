from django.forms import ValidationError
from watchlist.models import WatchList, StreamPlatform, Review
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins, generics
from watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from watchlist.api.permissions import AdminOrReadOnly, IsAuthorOrReadOnly
from watchlist.api.pagination import CustomPagination, WatchlistLOPagination
from user_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # def get_queryset(self):
    #     keyword = self.kwargs['username']
    #     return Review.objects.filter(review_user__username = keyword)
    
    def get_queryset(self):
        keyword = self.request.query_params.get('username', None)
        if keyword:
            return Review.objects.filter(review_user__username = keyword)
    

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [AdminOrReadOnly]
    throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        
        user = self.request.user
        # print(user)
        # print('----------------------------------------------------------------')
        check_user = Review.objects.filter(watchlist=watchlist, review_user=user)
        if check_user.exists():
            # print('already exists')
            raise ValidationError("You have already reviewed")
            # return Response({"error": "You have already reviewed this movie"}, status=status.HTTP_400_BAD_REQUEST)
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.number_rating = watchlist.number_rating + 1
        # print(watchlist.number_rating)
        watchlist.save()
        
        return serializer.save(watchlist=watchlist, review_user=user)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['review_user__username', 'active']
    filter_backends = [filters.SearchFilter]
    search_fields = ['review_user__username', 'active']
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        platform = StreamPlatform.objects.all()
        data = StreamPlatformSerializer(platform, many=True).data
        response = {
                "status": "valid",
                "message": "Platforms found",
                "data": data,
            }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "valid",
                "message": "Platform created",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status": "invalid",
                "message": "Unable to create platform",
                "error":serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
class StreamPlatformDetail(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request, id):
        try:
            platform = StreamPlatform.objects.get(pk=id)
        except platform.DoesNotExist:
            res_data = {'status':'invalid','message':'Platform not found'}
            return Response(res_data, status=status.HTTP_404_NOT_FOUND)
        data = StreamPlatformSerializer(platform).data
        res_data = {
            "status": "valid",
            "message": "Platform found",
            "data": data,
        }
        return Response(res_data)
    
    def put(self, request, id):
        try:
            platform = StreamPlatform.objects.get(pk=id)
        except StreamPlatform.DoesNotExist:
            res_data = {'status':'invalid','message':'Platform not found'}
            return Response(res_data, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = StreamPlatformSerializer(instance=platform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "status": "valid",
                    "message": "Platform updated successfully",
                    "data": serializer.data
                }
                return Response(data, status=200)
        
    def delete(self, request, id):
        try:
            platform = StreamPlatform.objects.get(pk=id)
        except StreamPlatform.DoesNotExist:
            res_data = {'status':'invalid','message':'Platform not found'}
            return Response(res_data, status=status.HTTP_404_NOT_FOUND)
        else:
            platform.delete()
            data = {'status':'valid','message':'Platform deleted successfully'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
          
          
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']  
    pagination_class = WatchlistLOPagination

class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        data = WatchListSerializer(movies, many=True).data
        response = {
                "status": "valid",
                "message": "Watchlist found",
                "data": data,
            }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "valid",
                "message": "Movie created successfully",
                "data": serializer.data
            }
            return Response(data, status=201)
        else:
            data = {
                "status": "invalid",
                # "message": serializer.errors['non_field_errors'][0],
                "data": serializer.errors
            }
            return Response(data)
        

class WatchDetails(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request, id):
        try:
            movie = WatchList.objects.get(pk=id)
        except WatchList.DoesNotExist:
            res_data = {'status':'invalid', 'message':'movie not found'}
            return Response(res_data, status=status.HTTP_404_NOT_FOUND)
        data = WatchListSerializer(movie).data
        return Response(data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        movie = WatchList.objects.get(pk=id)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        movie = WatchList.objects.get(pk=id)
        movie.delete()
        data = {
            "status": "valid",
            "message": "Movie deleted successfully",
        }
        return Response(data, status=204)

# @api_view(['GET'])
# def movies_list(request):
#     if request.method == 'GET':
#         movies = WatchList.objects.all()
#         data = MovieSerializer(movies, many=True).data
#         return Response(data, status=status.HTTP_200_OK)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, id):
#     if request.method == 'GET':
#         try:
#             movie = WatchList.objects.get(pk=id)
#         except Movie.DoesNotExist:
#             res_data = {'status':'invalid', 'message':'movie not found'}
#             return Response(res_data, status=status.HTTP_404_NOT_FOUND)
#         data = MovieSerializer(movie).data
#         return Response(data, status=status.HTTP_200_OK)
    
#     if request.method == 'PUT':
#         movie = WatchList.objects.get(pk=id)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':
#         movie = WatchList.objects.get(pk=id)
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
