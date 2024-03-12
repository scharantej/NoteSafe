## Flask Application Design

### HTML Files

- **Landing Page (`index.html`):**
  - Contains login form for registered users.
  - Provides a call-to-action button for new user registration.

- **Registration Page (`registration.html`):**
  - Form to collect user information for registration.
  - Includes password validation and recaptcha for security.

- **Home Page (`home.html`):**
  - User dashboard accessible after login.
  - Interface to create, edit, and organize notes.
  - Search and filtering options for note management.

### Routes

- **Login Route (`/login`):**
  - Validates user credentials and creates a session upon successful login.
  - Redirects to the home page on successful login, otherwise displays an error message.

- **Registration Route (`/register`):**
  - Stores user-provided information in the database.
  - Triggers an email verification process for the user.

- **Logout Route (`/logout`):**
  - Invalidates the user's session and logs the user out, redirecting to the landing page.

- **Create Note Route (`/create-note`):**
  - Handles user requests to create a new note, storing it in the database.
  - Redirects to the home page after note creation.

- **Edit Note Route (`/edit-note/<note_id>`):**
  - Loads an existing note for editing based on its ID.
  - Allows users to modify and update the note, redirecting to the home page on successful update.

- **Delete Note Route (`/delete-note/<note_id>`):**
  - Deletes a note based on its ID from the database.
  - Redirects to the home page after note deletion.

- **Search Notes Route (`/search-notes`):**
  - Performs a full-text search on notes based on user input.
  - Returns a list of matching notes in the search results.

- **Tag Notes Route (`/tag-notes`):**
  - Allows users to add and remove tags to notes, enhancing organization and filtering.
  - Redirects to the home page after tag updates.