// Get all the submit buttons on the page
const submitButtons = document.querySelectorAll('form button[id="countdownToDelete"]');

// Loop through each submit button and attach a click event listener
submitButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Disable the submit button
        button.disabled = true;

        // Set the countdown timer to 5 seconds
        let timeLeft = 7;
        let countdown = setInterval(() => {
            // Update the button text with the remaining time
            button.textContent = `Deleting in ${timeLeft} seconds...`;

            // Decrement the time left
            timeLeft--;

            // If the countdown has reached 0, stop the timer and submit the form
            if (timeLeft === 0) {
                clearInterval(countdown);
                button.closest('form').submit();
            }
        }, 1000);

        // Create a cancel button that will appear during the countdown
        const cancelButton = document.createElement('button');
        cancelButton.textContent = 'Cancel';
        cancelButton.classList.add('btn', 'btn-warning');
        cancelButton.style.marginLeft = '.5rem';
        button.after(cancelButton);

        // Attach a click event listener to the cancel button to stop the countdown and reset the form
        cancelButton.addEventListener('click', (event) => {
            // Prevent the default form submission behavior
            event.preventDefault();

            // Stop the countdown timer
            clearInterval(countdown);

            // Remove the cancel button
            cancelButton.remove();

            // Enable the submit button and reset the button text
            button.disabled = false;
            button.textContent = 'Delete';

            // Reset the form to its initial state
            const form = button.closest('form');
            form.reset();
        });

        // Attach a click event listener to the button again to stop the countdown and show the cancel button
        button.addEventListener('click', (event) => {
            // Prevent the default form submission behavior
            event.preventDefault();

            // Stop the countdown timer
            clearInterval(countdown);

            // Show the cancel button
            cancelButton.style.display = 'inline-block';

            // Enable the submit button and update the button text
            button.disabled = false;
            button.textContent = 'Deleting...';
        });
    });
});