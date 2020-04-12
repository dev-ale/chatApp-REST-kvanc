<template>
  <div id="app">
  <h1>ChatApp REST - kvanc 2020</h1>

    <h3>Users:</h3>
    <input type="text" v-model="userName" @keyup.enter="signIn">
    <ul>
      <li v-for="user of users" :key="user.ip">{{ user.username }}</li>
    </ul>
  </div>
</template>

<script>
import axios from "axios"

const userUrl = 'http://127.0.0.1:5000/api/users';

export default {
  name: 'App',
  data() {
    return {
      users: [],
      userName: '',
      ip: ''
    }
  },
  async created() {
    try {
      const res = await axios.get(userUrl);
      this.getUsersIP();
      this.users = res.data;
    } catch(e) {
      console.error(e)
    }
  },
  methods: {
    async signIn() {
      try {
        const res = await axios.put(userUrl, {username: this.userName, ip: this.ip});

        this.users = [...this.users, res.data];
        this.userName = '';
        this.ip = '';
        window.location.reload();
      } catch(e) {
        console.error(e)
      }
    },
    getUsersIP() {
      fetch('https://api.ipify.org?format=json')
              .then(x => x.json())
              .then(({ ip }) => {
                this.ip = ip;
                console.log(ip);
              });
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
