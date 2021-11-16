from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    
    #notes
    path('notes/',views.notes,name="notes"),
    path('delete-note/<int:pk>/',views.deleteNote,name="delete-note"),
    path('note/<int:pk>/',views.NoteDetailView.as_view(),name="note"),

    #homework
    path('homework/',views.homeWork,name="homework"),
    path('update-homework/<int:pk>/',views.update_homework,name="update-homework"),
    path('delete-homework/<int:pk>/',views.delete_homework,name="delete-homework"),

    #youtube
    path('youtube/',views.youtube,name="youtube"),

    #todo
    path('todo/',views.todo,name="todo"),
    path('updateTodo/<int:pk>/',views.updateTodo,name="update-todo"),
    path('deleteTodo/<int:pk>/',views.deleteTodo,name="delete-todo"),

    #books
    path('books',views.books,name='books'),

    #dictionary
    path('dictionary',views.dictionary,name="dictionary"),

    #wikipedia
    path('wiki/',views.wiki,name="wiki"),

    #conversion
    path('conversion/',views.conversion,name="conversion"),

    
]