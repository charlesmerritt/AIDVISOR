document.addEventListener('DOMContentLoaded', function() {
    // Cache DOM references
    let sideWindow = document.getElementById('sideWindow');
    let toggleButton = document.getElementById('toggleButton');
    let userInput = document.getElementById('userInput');

    // Functionality for toggleButton
    toggleButton.addEventListener('click', function() {
        // Toggle a class that indicates the sidebar is shown
        sideWindow.classList.toggle('shown');

        // Adjust the toggle button position based on the sidebar's state
        toggleButton.style.left = sideWindow.classList.contains('shown') ? '250px' : '0px';
    });

    // Delegate event listener for prompt buttons
    document.addEventListener('click', function(e) {
        if (e.target && e.target.matches('.prompt-btn')) {
            let promptText = e.target.textContent || e.target.innerText;
            let modifiedText = promptText.substring(2).trim(); // Remove the first two characters (emoji and space)
            userInput.value = modifiedText; // Populate the textarea
        }
    });
});
