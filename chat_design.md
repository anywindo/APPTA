# Interactive Chat Feature Design (chat_demo.py)

## Understanding Summary
- **What is being built:** An interactive, multi-session Gradio web application acting as a chat interface for Alice and Bob, alongside a Database Browser view.
- **Why it exists:** To serve as an educational tool that demonstrates step-by-step how the project's ECDH and AES-GCM cryptography works in real-time.
- **Who it is for:** Developers, reviewers, or students wanting to understand the inner workings of the E2EE implementation.
- **Key constraints:** It utilizes the exact same cryptographic primitives (`src.crypto`, `src.protocol`) as the main experimental instrument. 
- **Explicit non-goals:** This will *not* replace the main benchmark scripts. It avoids complex Key Management Systems.

## Assumptions
- **Scale/Performance:** It only needs to support a few local connections for demonstration purposes.
- **Security:** Relies entirely on the existing cryptographic implementations. Storing public keys and messages in SQLite is for simulating a network and server, not for building a production secure storage system. Session keys reside strictly in memory.
- **Database:** SQLite (`chat.db`) will be used as a mock central server. 

## Decision Log
1. **Interactive vs Scripted:** Decided to make it a truly interactive Gradio web application rather than a hardcoded scripted demo.
2. **Storage mechanism:** Decided to use SQLite to store ciphertexts and public keys, simulating an untrusted server.
3. **Session Keys:** Decided to keep derived AES-GCM session keys in application memory only (they are lost on restart), mirroring true E2EE practices.
4. **Architecture:** Decided on a multi-session Gradio app where users select an identity (Alice, Bob, or Database Browser) on startup. This allows opening multiple browser windows to see the live interaction from different perspectives.

## Final Design

### 1. SQLite Database Schema (`chat.db`)
The database acts as our untrusted "Server".
- **Table `public_keys`:**
  - `user` (TEXT PRIMARY KEY) - "Alice" or "Bob"
  - `public_key` (BLOB) - Serialized public key
- **Table `messages`:**
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `sender` (TEXT) - "Alice" or "Bob"
  - `nonce` (BLOB) - 12 bytes
  - `ciphertext` (BLOB) - Variable length
  - `tag` (BLOB) - 16 bytes
  - `timestamp` (DATETIME)

### 2. Gradio Interface Structure
When the user accesses the Gradio URL, they are presented with a choice:
- **Login as Alice:** 
  - Generates her key pair.
  - Saves her public key to the DB.
  - Checks the DB for Bob's public key; if found, computes the shared AES-GCM key.
  - Displays a chat UI (`gr.Chatbot`) and a text input.
  - Displays a "Crypto Log" panel showing verbose steps (e.g., nonce generation, encryption).
- **Login as Bob:**
  - Mirrors Alice's setup.
- **Database Browser (Server View):**
  - A view that periodically refreshes and displays the contents of the `messages` and `public_keys` tables.
  - Visually proves that the server only possesses random bytes (ciphertexts) and cannot read the plaintext messages.

### 3. Data Flow (Alice sending to Bob)
1. Alice types a message and clicks send.
2. In Alice's memory: The app uses `src.crypto` to generate a 12-byte nonce, encrypt the message with AES-256-GCM using the shared key, producing the ciphertext and 16-byte tag.
3. The Crypto Log updates in Alice's UI.
4. The raw `nonce`, `ciphertext`, and `tag` are inserted into the SQLite `messages` table.
5. Bob's UI (via Gradio's periodic polling or refresh mechanism) detects a new row in `messages`.
6. In Bob's memory: The app uses `src.crypto` to decrypt the ciphertext using the shared key.
7. The plaintext is added to Bob's chat history.
8. The Crypto Log updates in Bob's UI.
