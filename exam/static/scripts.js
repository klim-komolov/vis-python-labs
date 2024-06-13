
    const deleteModal = document.getElementById('deleteModal');
    deleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const bookId = button.getAttribute('data-book-id');
        const bookTitle = button.getAttribute('data-book-title');

        const modalTitle = deleteModal.querySelector('.modal-title');
        const modalBodySpan = deleteModal.querySelector('.modal-body #bookTitle');
        const deleteForm = deleteModal.querySelector('#deleteForm');

        modalTitle.textContent = 'Удаление книги';
        modalBodySpan.textContent = bookTitle;
        deleteForm.action = '/book/delete/' + bookId;
    });
