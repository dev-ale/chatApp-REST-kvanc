<template>
  <div id="app">
    <NewUser/>
    <h1>ChatApp REST - kvanc 2020</h1>

      <h3>Users:</h3>
      Logged In: <span style="color: red; font-weight: bold">{{ loggedIn }}</span> <br>
      <input placeholder="username" type="text" v-if="!loggedIn" v-model="userName" @keyup.enter="signIn">
      <button v-if="loggedIn" @click="signOut">Logout</button>
      <button v-if="!loggedIn" @click="signIn">Sign In</button>
      <ul>
        <li v-for="user of users" :key="user.ip"><span style="font-weight: bold; font-size: 1.2em;">{{ user.username }}</span> : {{ user.ip }}</li>
      </ul>

    <div>
      <h3>Chat:</h3>
      <p v-if="this.messages.length < 1">Keine Nachrichten, bis jetzt...</p>
      <p v-if="!loggedIn">Bitte zuerst einloggen...</p>

      <ul v-if="loggedIn">
        <li v-for="message of messages" :key="message.message"><span style="font-weight: bold">{{ message.username }}</span> : {{ message.message }} <span style="font-size: 0.8em; color: lightgrey;">10:34</span></li>
      </ul>
      <input v-if="loggedIn" placeholder="message" type="text" v-model="messageContent" @keyup.enter="sendMessage">
    </div>

  </div>
</template>

<script>
import axios from "axios"
import NewUser from "./components/NewUser.vue"


const userUrl = 'http://127.0.0.1:5000/api/users';
const messageUrl = 'http://127.0.0.1:5000/api/messages';

export default {
  name: 'App',
  components: {
    NewUser
  },
  data() {
    return {
      users: [], // Array of Objects with actual Users (ip, username)
      messages: [], // Array of Objects with actual Messages (username, message)
      userName: '',
      ip: '',
      messageContent: '',
      loggedIn: false
    }
  },
  async created() {
    this.getUsersIP();
    this.getUsers();
    this.getMessages();
    this.updateData(5000);
  },
  methods: {
    // Method to fetch Userlist and Messages every x second
    updateData(interval) {
      setInterval(() => {
        this.getUsers();
        this.getMessages();
        console.log("fetched user list and messages")
      }, interval);
    },
    // Fetches the logged in Users from Backend
    async getUsers() {
      try {
        const users = await axios.get(userUrl);
        this.users = users.data;
      } catch(e) {
        console.error(e)
      }
    },
    // Fetches theMessages from Backend
    async getMessages() {
      try {
        const mes = await axios.get(messageUrl);
        this.messages = mes.data;
      } catch(e) {
        console.error(e)
      }
    },
    // addd the User to The Userlist in Backend
    async signIn() {
      try {
        const res = await axios.put(userUrl, {username: this.userName, ip: this.ip});
        this.users = [...this.users, res.data];
        this.loggedIn = true;
        this.getUsers();
      } catch(e) {
        console.error(e)
      }
    },

    // Removes User from the List
    async signOut() {
      try {
        this.loggedIn = false;
        this.userName = '';
        // TODO: Should remove the User from the List
      } catch(e) {
        console.error(e)
      }
    },
    // Gets Users external IP for as a ID
    getUsersIP() {
      fetch('https://api.ipify.org?format=json')
              .then(x => x.json())
              .then(({ ip }) => {
                this.ip = ip;
              });
    },
    // Gets the Actual Time in Format (HH:MM)
    getTime() {
      let time = new Date().toJSON().slice(11,19).replace(/-/g,'/');
      return time.toString();
    },
    // Adds a Message to the List with the actual Username
    // TODO: In every message a timestamp should be added at the end
    async sendMessage() {
      try {
        const res = await axios.post(messageUrl, {username: this.userName, message: this.messageContent});
        this.messages = [...this.messages, res.data];
        this.messageContent = '';
        this.getMessages();
      } catch(e) {
        console.error(e)
      }
    },
  },

}
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  li {
    list-style: none;
  }
  ul {
    margin: 0;
    padding: 0;
  }

</style>
