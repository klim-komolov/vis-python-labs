
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

    $('#deleteModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) 
        var bookId = button.data('bookid') 
        var bookTitle = button.data('booktitle') 
        var modal = $(this)
        modal.find('.modal-body #bookTitle').text(bookTitle)
        modal.find('.modal-footer form').attr('action', '/book/delete/' + bookId)
    })