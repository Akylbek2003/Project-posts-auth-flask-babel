function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ noteId: noteId }),  // noteId с маленькой буквы
    }).then((_res) => {
        window.location.href = "/";
    });
}

