from django.db import router
from rest_framework import urlpatterns, routers
from django.conf.urls import include, url
# from django.conf.urls import patterns
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import MyNoteImageDeleteView, NoteViewSet, MyNoteListView, PeerNotesView, MyNoteDeleteView, NoteCreateView, MyNoteUpdateView
from .views import note_add, notes, peer_notes, note_edit, peer_detail
from .models import Note
from .utils import CustomReadOnlyRouter


router = CustomReadOnlyRouter()
# router = routers.DefaultRouter()
router.register(r'note', NoteViewSet, basename='note')

urlpatterns = [

    url(r"^notes/$", login_required(notes), name="note_list"),
    url(r"^notes/add/$", login_required(note_add), name="note_add"),
    url(r"^notes/edit/(?P<pk>\d+)/$", login_required(note_edit), name="note_edit"),
    url(r"^notes/peer/$", login_required(peer_notes), name="peer_notes"),
    url(r"^notes/peer_detail/(?P<pk>\d+)/$", login_required(peer_detail), name="peer_detail"),      

    url(r'v0/', include((router.urls, 'note'), namespace='v0')),
    

    path(r'note_delete/<str:id>/', MyNoteDeleteView.as_view()),
    path(r'note_image_delete/<str:id>/', MyNoteImageDeleteView.as_view()),
    path(r'note_update/<str:id>/', MyNoteUpdateView.as_view()),
    path(r'note_create/', NoteCreateView.as_view(), name='note_create'),
    path(r'peer_notes/<str:course_id>/', PeerNotesView.as_view()),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path(r'notes/<str:course_id>/', MyNoteListView.as_view()),

]



