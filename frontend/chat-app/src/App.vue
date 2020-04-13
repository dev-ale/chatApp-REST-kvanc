<template>
  <div id="app">
    <NewUser/>
    <h1>ChatApp REST - kvanc 2020</h1>

      <h3>Users:</h3>
      Logged In: <span style="color: red; font-weight: bold">{{ loggedIn }}</span> <br>
      <input placeholder="username" type="text" v-if="!loggedIn" v-model="userName" @keyup.enter="signIn">
      <button @click="signOut">Logout</button>
      <ul>
        <li v-for="user of users" :key="user.ip"><span style="font-weight: bold; font-size: 1.2em;">{{ user.username }}</span> : {{ user.ip }}</li>
      </ul>

      <h3>Chat:</h3>
      <p v-if="this.messages.length < 1">Keine Nachrichten, bis jetzt...</p>
      <ul>
        <li v-for="message of messages" :key="message.message"><span style="font-weight: bold">{{ message.username }}</span> : {{ message.message }} <span style="font-size: 0.8em; color: lightgrey;">10:34</span></li>
      </ul>
      <input placeholder="message" type="text" v-model="messageContent" @keyup.enter="sendMessage">
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
      users: [],
      messages: [],
      userName: '',
      ip: '',
      messageContent: '',
      loggedIn: false
    }
  },
  async created() {
    try {
      const users = await axios.get(userUrl);
      const mes = await axios.get(messageUrl);
      this.getUsersIP();
      this.getDate();
      this.users = users.data;
      this.messages = mes.data;
    } catch(e) {
      console.error(e)
    }
  },
  methods: {
    async signIn() {
      try {
        const res = await axios.put(userUrl, {username: this.userName, ip: this.ip});

        this.users = [...this.users, res.data];
        this.loggedIn = true;
        const users = await axios.get(userUrl);
        this.users = users.data;
        this.loggedIn = true;
        console.log(this.userName);
      } catch(e) {
        console.error(e)
      }
    },
    async signOut() {
      try {

        this.loggedIn = false;
        //window.location.reload();
        this.userName = '';

      } catch(e) {
        console.error(e)
      }
    },
    getUsersIP() {
      fetch('https://api.ipify.org?format=json')
              .then(x => x.json())
              .then(({ ip }) => {
                this.ip = ip;

              });
    },
    getDate() {
      let currentDateWithFormat = new Date().toJSON().slice(11,19).replace(/-/g,'/');
      console.log(currentDateWithFormat);
      return currentDateWithFormat.toString();
    },
    async sendMessage() {
      try {

        const res = await axios.post(messageUrl, {username: this.userName, message: this.messageContent});
        console.log(this.userName);
        console.log(this.messageContent);
        this.messages = [...this.messages, res.data];
        this.messageContent = '';

        const mes = await axios.get(messageUrl);
        this.messages = mes.data;
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
