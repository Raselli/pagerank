document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send composed e-mail
  document.querySelector('form').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';  
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Load all mails related to this inbox
    emails.forEach(email => {

          // create sub-div and add class to it
          const element = document.createElement('div');
          element.classList.add('mail_frame');

          load_mails(email);
    });
  })

  // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
}

// creates a div filled with divs containing all info about an email
function load_mails(email) {

  // Create DIV for an e-mail
  const email_box = document.createElement('div');
  email_box.classList.add('mail_frame');
  email_box.setAttribute("id", `${email.id}`);
  document.querySelector('#emails-view').append(email_box);        
  
  // Change BackgroundColor based on read / not read
  if (email.read === true) {
    email_box.style.backgroundColor = 'LightGray';
  } else {
    email_box.style.backgroundColor = 'white';
  }
  
  // Create and populate HTML elements inside e-mail DIV
  const mail_info = [email.subject, email.sender, email.timestamp, email.body]
  for (let i = 0; i < mail_info.length; i++) {         
    var span = document.createElement('span');
    span.innerHTML = mail_info[i];
    span.classList.add('mailbox_column')
    email_box.append(span);
  }

  // Load content of e-mail
  email_box.addEventListener('click', function() {

    view_mail(email.id);
  });
}

// Send Mail
function send_mail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value,
        read: false
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
}


// TODO:
// split view_mail:
// - function: handle query selectors = onclick events
// - function: create elements and populate
// - function: button archivate
// - function: button reply

//View Mail
function view_mail(id) {

  // Show E-mails Content, Hide Mailboxes,
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').innerHTML = '';
  document.querySelector('#email-view').style.display = 'block'; 

  // Get e-mail data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    // Mark e-mail as 'read'
    if (email.read === false) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }

// TODO: replace 2 arrays by dicts
    // List of items for createElement (below)
    const mail_info = [email.subject, email.sender, email.recipients, email.timestamp]
    const mail_deco = ["Subject: ", "From: ", "To: ", ""]
    
    // Create and populate HTML-elements 
    for (let i = 0; i < mail_info.length; i++) {
      var b = document.createElement('b');            
      var div = document.createElement('div');
      b.innerHTML = mail_deco[i];
      div.innerHTML = mail_info[i];
      div.prepend(b);
      document.getElementById('email-view').append(div);
    }

    // Line & e-mail body
    var line = document.createElement('hr');
    var body = document.createElement('div');
    body.classList.add('email_body');
    body.innerHTML = email.body

    // Reply Button
    var reply_button = document.createElement('button');
    reply_button.type = 'submit';
    reply_button.className = 'btn btn-primary';
    reply_button.setAttribute("id", `r_${email.id}`);
    reply_button.innerHTML = 'Reply';

    // Archivation Button
    var archive_button = document.createElement('button');
    archive_button.type = 'submit';
    archive_button.className = 'btn btn-primary';
    archive_button.setAttribute("id", `a_${email.id}`);
    if (email.archived === false) {
      archive_button.innerHTML = 'Archive';
    } else {
      archive_button.innerHTML = 'Unarchive';
    }
    document.getElementById('email-view').append(reply_button, archive_button, line, body);
    
    // Archivation Event
    archive_button.addEventListener('click', function() {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(result => {
          // Print result
          console.log(result);
          load_mailbox('inbox');
      });
    })

    // Reply Event
    reply_button.addEventListener('click', function() {
        document.querySelector('#email-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';
      
        // Pre-fill the composition fields
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
        if (email.subject.substring(0, 4) == 'Re: ') {
          document.querySelector('#compose-subject').value = email.subject;
        } else {
          document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
        }
    })
  })

  // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
};
