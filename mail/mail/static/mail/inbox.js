document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

// Send Mail
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('form').onsubmit = function() {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    })

    // Catch any errors and log them to the console
    .catch(error => {
      console.log('Error:', error);
    });

    load_mailbox('sent');    
    // Prevent default submission
    return false;
  };
});

// Mailbox
  // if user click on mailbox: INBOX, SENT, ARCHIVE load the requested box
  // fetch /emails/<mailbox> method: GET
  // when visit a mailbox -> API should fetch latest mails
  // active Mailbox name should appear on top: html -> h1 or h2 ?
  // render each mail in own <div> with: mailaddress of sender, subject, timestamp
    // Mail: if unread -> background-color = white. else: bgc = grey

//View Mail
  // when user clicks on mail -> open mail
  // fetch /emails/<email_id> method: GET
  // display: sender, recipients, subject, timestamp, body
  // @inbox.html: add <div> with id for display/hide email body
    // if email clicked on: fetch /emails/<email_id> method: PUT -> read === True

// Archive and Unarchive


  // @Inbox: button for archivation.
  // @Archive: button for unarchive
  // fetch /emails/<email_id> method: PUT -> archive === True
  // After archive/unarchive: load Inbox of User

// Reply
  // @active mail_id body: add Reply button
  // Reply Button -> open email composition form
    // pre-fill "recipient" with reply to prev address
    // pre-fill "subject" with "Re: foo"
      // if subject begins with a prev. "Re:": add no "Re:"
    // pre-fill body with "On ${timestamp} ${recipient} wrote:"
