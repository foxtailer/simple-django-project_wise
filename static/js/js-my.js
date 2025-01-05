let selectedId = null;
let previousElement = null;

const wisdomElements = document.querySelectorAll('.my_wisdom');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


wisdomElements.forEach(element => {
    element.addEventListener('click', () => {
        selectedId = element.id;

        if (previousElement) {
            previousElement.style.backgroundColor = '';
        }

        element.style.backgroundColor = '#323232';
        previousElement = element;
    });
});


function deletePost() {
    fetch('', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ post_id: selectedId })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Post deleted successfully.', data.id);
        document.getElementById(selectedId).remove();
    })
    .catch(error => console.error('Error:', error));
}


function closeForm() {
    document.getElementById("popupForm").style.display = "none";
}


function openForm() {
    document.getElementById("popupForm").style.display = "block";

    if (selectedId) {
        let text = document.getElementById(selectedId).innerText;
        document.getElementById("write-form__text").value = text;
        document.getElementById("post_id").value = selectedId;
    };
}
