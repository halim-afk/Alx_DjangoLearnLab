
python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.views import View
from django.views.generic.detail import DetailView

from.models import Book, Library
from.forms import BookForm, RegisterForm

# ===== عروض إدارة الكتب =====
@permission_required('relationship_app.can_add_book', login_url='/login/')
def add_book(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_books')
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_change_book', login_url='/login/')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('list_books')
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_delete_book', login_url='/login/')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ===== تفاصيل المكتبة =====
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# ===== إدارة صلاحيات المستخدم =====
def check_role(role):
    def decorator(user):
        return user.is_authenticated and getattr(user.userprofile, 'role', None) == role
    return user_passes_test(decorator)

@check_role('Admin')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@check_role('Librarian')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@check_role('Member')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# ===== التسجيل =====
def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('login')
    return render(request, 'relationship_app/register.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'relationship_app/register.html', {'form': form})
