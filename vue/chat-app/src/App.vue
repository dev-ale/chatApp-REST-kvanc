<template>
  <v-app>
    <vue-title v-if="!userName" title='kvanc Chat App'></vue-title>
    <vue-title v-if="loggedIn" :title="'kvanc Chat App ' + userName"></vue-title>
    <v-app-bar app dark :color="dynamic">
      <v-toolbar-title v-if="userName === 'admin' && loggedIn">Admin</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-title>ChatApp REST - kvanc 2020</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-chip v-if="serverConnected" style="margin-left: 5px" color="success" @click="openSwaggerSite">{{ this.Url }}</v-chip>
      <v-chip v-if="!serverConnected" style="margin-left: 5px" color="error" @click="openSwaggerSite">{{ this.Url }}</v-chip>

    </v-app-bar>



    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar
                      :color="dynamic"
                      dark
                      flat
              >
                <v-toolbar-title>Users</v-toolbar-title>
                <v-spacer/>
                <div v-if="this.users.length > 0">
                  {{ this.users.length }}
                </div>
              </v-toolbar>
              <v-card-text>
                <div style="text-align: center">
                  <p v-if="this.users.length < 1 && serverConnected">Keine User online</p>
                  <p v-if="!serverConnected">Keine Verbindung zum Server</p>
                </div>


                <div v-if="serverConnected">
                  <v-text-field v-if="!loggedIn" label="Benutzername" outlined dense v-model="userName" @keyup.enter="checkAdmin">
                    <template slot="append">

                      <v-btn v-if="userName !== 'admin'" icon color="dynamic" style="margin-bottom: 10px;" @click="checkAdmin">
                        <v-icon left>mdi-login-variant</v-icon>
                      </v-btn>

                    </template>
                  </v-text-field>
                  <v-text-field v-if="!loggedIn && userName === 'admin'" label="Passwort" v-model="password" outlined dense type="password" @keyup.enter="checkAdmin">
                    <template slot="append">
                      <v-btn icon color="red" style="margin-bottom: 10px;" @click="checkAdmin">
                        <v-icon left>mdi-login-variant</v-icon>
                      </v-btn>
                    </template>
                  </v-text-field>
                  <v-alert
                          :value="alert"
                          color="error"
                          dismissible
                          text
                          dark
                          icon="mdi-login-variant"
                          transition="scale-transition"
                  >Passwort falsch!</v-alert>
                  <v-list>
                    <v-list-item v-for="user of users" :key="user.username">
                      <v-icon>mdi-account</v-icon>
                      <span style="font-weight: bold; font-size: 1.2em; cursor: pointer"> {{ user.username }} </span>
                      <v-btn @click="receiver = user.username" outlined depressed x-small dark color="#00695c" style="margin-left: 5px" v-if="loggedIn === true && userName !== user.username && receiver !== user.username">Privater Chat</v-btn>

                      <v-btn @click="receiver = 'all'"  depressed x-small dark color="#00695c" style="margin-left: 5px" v-if="loggedIn === true && userName !== user.username && receiver === user.username">Privater Chat</v-btn>

                      <v-btn depressed x-small v-if="receiver === user.username && userName !== user.username" @click="receiver = 'all'">X</v-btn>
                      <v-btn depressed x-small color="error" style="margin-left: 5px" v-if="user.username === userName && loggedIn" @click="signOut">Logout</v-btn>
                    </v-list-item>
                  </v-list>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="8">
            <div style="text-align: center">
              <p v-if="!loggedIn && serverConnected">Bitte zuerst einloggen</p>
            </div>

            <v-layout v-if="this.userName === 'admin' && loggedIn" style="text-align: center" justify-center>
              <v-flex xs12 md4 >
                <v-switch v-model="showAllMessages" inset class="switch-center" label="zeige mir alle Privatnachrichten"></v-switch>
              </v-flex>
            </v-layout>


<!--             Normaler Chat-->
            <v-card v-if="loggedIn && serverConnected && this.receiver === 'all'  && !showAllMessages" class="elevation-12">
              <v-toolbar :color="dynamic" dark flat>
                <v-toolbar-title>Öffentlicher Chat</v-toolbar-title>
                <v-spacer/>
              </v-toolbar>
              <v-card-text>
                <p v-if="this.filterAll.length < 1">Keine Nachrichten</p>
                <v-list>
                  <v-list-item v-for="message of filterAll" :key="message.time">

                    <div v-if="message.message.toLocaleString().startsWith('http')">
                      <span style="font-weight: bold">{{ message.username }} : </span>
                      <v-img max-width="150" max-height="150" :src="message.message"></v-img>
                    </div>
                    <div v-if="!message.message.toLocaleString().startsWith('http')">
                      <!--Own Messages-->
                      <div v-if="message.username === userName">
                        <span style="font-weight: bold">{{ message.username }} : </span>

                        <v-chip style="margin-left: 5px" color="primary">
                          {{ message.message }}
                          <span style="font-size: 0.7em; margin-left: 3px"> <br> {{ message.time }}</span>
                        </v-chip>
                      </div>

                      <!--Chatbot Messages-->
                      <div v-else-if="message.username === 'Chatbot' && chatbotMessages">
                        <v-chip small style="margin-left: 5px" color="lightgrey">
                          {{ message.message }}
                        </v-chip>
                      </div>

                      <!--Private Messages-->
                      <div v-else-if="message.receiver !== 'all' && message.username !== 'Chatbot' && message.username !== userName">
                        <span style="font-weight: bold">{{ message.username }} @ {{ message.receiver }} </span>
                        <v-chip @click="receiver = message.username" style="margin-left: 5px" dark color="#00695c">
                          {{ message.message }}
                          <span style="font-size: 0.7em; margin-left: 3px"> <br> {{ message.time }}</span>
                        </v-chip>
                      </div>

                      <!--Other Messages-->
                      <div v-else-if="message.receiver === 'all' && message.username !== 'Chatbot' && message.username !== userName">
                        <span style="font-weight: bold">{{ message.username }} : </span>
                        <v-chip style="margin-left: 5px"  color="success">
                          {{ message.message }}
                          <span style="font-size: 0.7em; margin-left: 3px"> <br> {{ message.time }}</span>
                        </v-chip>
                      </div>
                    </div>


                  </v-list-item>
                </v-list>
                <br>
                <div v-if="loggedIn && gifSelected" class="gif-container">
                  <img height="50" v-for="gif in gifs" :src="gif" :key="gif.id" @click="clickedOnGif(gif)">
                </div>
                <v-text-field color="primary" v-if="loggedIn && !gifSelected" :label="'Nachricht an: ' + this.receiver" dense outlined v-model="messageContent" @keyup.enter="sendMessage">
                  <template slot="prepend">
                    <v-btn v-if="gifSelected" icon @click="gifSelected = false">
                      <v-icon color="dynamic" left>mdi-chat-processing-outline</v-icon>
                    </v-btn>
                    <v-btn v-if="!gifSelected" icon @click="gifSelected = true">
                      <v-icon left>mdi-gif</v-icon>
                    </v-btn>
                  </template>

                  <template slot="append">
                    <v-btn v-if="!this.messageContent.length == 0" icon color="primary" style="margin-bottom: 10px;" @click="sendMessage">
                      <v-icon left>mdi-send-outline</v-icon>
                    </v-btn>
                  </template>
                </v-text-field>
                <v-text-field color="primary" v-if="loggedIn && gifSelected" label="GIF suchen" dense outlined v-model="searchTerm" @keyup.enter="getGifs">
                  <template slot="prepend">
                    <v-btn v-if="gifSelected" icon @click="gifSelected = false">
                      <v-icon color="dynamic" left>mdi-chat-processing-outline</v-icon>
                    </v-btn>
                    <v-btn v-if="!gifSelected" icon @click="gifSelected = true">
                      <v-icon left>mdi-gif</v-icon>
                    </v-btn>
                  </template>
                  <v-btn v-if="!this.messageContent.length == 0" icon color="primary" style="margin-bottom: 10px;" @click="sendMessage">
                    <v-icon left>mdi-send-outline</v-icon>
                  </v-btn>
                </v-text-field>
              </v-card-text>
            </v-card>

            <!--             Private Chat-->
            <v-card v-if="loggedIn && serverConnected && this.receiver !== 'all' && !showAllMessages" class="elevation-12">
              <v-toolbar color="#00695c" dark flat>
                <v-toolbar-title>Privater Chat mit: {{ this.receiver }}</v-toolbar-title>
                <v-spacer/>
                <v-btn color="#00695c" @click="receiver = 'all'">X</v-btn>
                  <!--TODO: Switch to turn of and on Chatbot Messages doesnt work yet-->
                  <!--<v-switch label="Chatbot" @change="changeChatbotStatus"></v-switch>-->
              </v-toolbar>
              <v-card-text>
                <p v-if="this.filterPrivate.length < 1">Keine Nachrichten</p>
                <v-list>
                  <v-list-item v-for="message of filterPrivate" :key="message.time">

                    <div v-if="message.message.toLocaleString().startsWith('http')">
                      <span style="font-weight: bold">{{ message.username }} : </span>
                      <v-img max-width="150" max-height="150" :src="message.message"></v-img>
                    </div>

                    <div v-if="!message.message.toLocaleString().startsWith('http')">
                      <!--Own Messages-->
                      <div v-if="message.username === userName">
                        <span style="font-weight: bold">{{ message.username }} : </span>
                        <v-chip style="margin-left: 5px" color="primary">
                          {{ message.message }}
                          <span style="font-size: 0.7em; margin-left: 3px"> <br> {{ message.time }}</span>
                        </v-chip>
                      </div>

                      <!--Chatbot Messages-->
                      <div v-else-if="message.username === 'Chatbot' && chatbotMessages">
                        <v-chip small style="margin-left: 5px" color="lightgrey">
                          {{ message.message }}
                        </v-chip>
                      </div>



                      <!--Other Messages-->
                      <div v-else-if="message.username !== 'Chatbot' && message.username !== userName">
                        <span style="font-weight: bold">{{ message.username }} : </span>
                        <v-chip style="margin-left: 5px"  color="success">
                          {{ message.message }}
                          <span style="font-size: 0.7em; margin-left: 3px"> <br> {{ message.time }}</span>
                        </v-chip>
                      </div>
                    </div>




                  </v-list-item>
                </v-list>
                <br>
                <div v-if="loggedIn && gifSelected" class="gif-container">
                  <img height="50" v-for="gif in gifs" :src="gif" :key="gif.id" @click="clickedOnGif(gif)">
                </div>
                <v-text-field color="primary" v-if="loggedIn && !gifSelected" :label="'Nachricht an: ' + this.receiver" dense outlined v-model="messageContent" @keyup.enter="sendMessage">
                  <template slot="prepend">
                    <v-btn v-if="gifSelected" icon @click="gifSelected = false">
                      <v-icon color="dynamic" left>mdi-chat-processing-outline</v-icon>
                    </v-btn>
                    <v-btn v-if="!gifSelected" icon @click="gifSelected = true">
                      <v-icon left>mdi-gif</v-icon>
                    </v-btn>
                  </template>

                  <template slot="append">
                    <v-btn v-if="!this.messageContent.length == 0" icon color="primary" style="margin-bottom: 10px;" @click="sendMessage">
                      <v-icon left>mdi-send-outline</v-icon>
                    </v-btn>
                  </template>
                </v-text-field>
                <v-text-field color="primary" v-if="loggedIn && gifSelected" label="GIF suchen" dense outlined v-model="searchTerm" @keyup.enter="getGifs">
                  <template slot="prepend">
                    <v-btn v-if="gifSelected" icon @click="gifSelected = false">
                      <v-icon color="dynamic" left>mdi-chat-processing-outline</v-icon>
                    </v-btn>
                    <v-btn v-if="!gifSelected" icon @click="gifSelected = true">
                      <v-icon left>mdi-gif</v-icon>
                    </v-btn>
                  </template>
                  <v-btn v-if="!this.messageContent.length == 0" icon color="primary" style="margin-bottom: 10px;" @click="sendMessage">
                    <v-icon left>mdi-send-outline</v-icon>
                  </v-btn>
                </v-text-field>
              </v-card-text>
            </v-card>


            <!--             Admin Chat-->
            <v-card v-if="loggedIn && serverConnected && showAllMessages" class="elevation-12">
              <v-toolbar :color="dynamic" dark flat>
                <v-toolbar-title>Admin Chat</v-toolbar-title>
                <v-spacer/>
              </v-toolbar>
              <v-card-text>
                <p v-if="this.filterAll.length < 1">Keine Nachrichten</p>
                <v-list>
                  <v-list-item v-for="message of messages" :key="message.time">

                    <div v-if="message.message.toLocaleString().startsWith('http')">
                      <span style="font-weight: bold">{{ message.username }} : </span>
                      <v-img max-width="150" max-height="150" :src="message.message"></v-img>
                    </div>

                    <div v-if="!message.message.toLocaleString().startsWith('http')">
                      <!--Own Messages-->
                      <div v-if="message.username === userName">
                        <span style="font-weight: bold">{{ message.username }} : </span>
                        <v-chip style="margin-left: 5px" color="primary">
                          {{ message.message }}
                          <span style="font-size: 0.7em; margin-left: 3px"> <br> {{ message.time }}</span>
                        </v-chip>
                      </div>

                      <!--Chatbot Messages-->
                      <div v-else-if="message.username === 'Chatbot' && chatbotMessages">
                        <v-chip small style="margin-left: 5px" color="lightgrey">
                          {{ message.message }}
                        </v-chip>
                      </div>

                      <!--Other Messages-->
                      <div v-else-if="message.receiver === 'all' && message.username !== 'Chatbot' && message.username !== userName">
                        <span style="font-weight: bold">{{ message.username }} : </span>
                        <v-chip style="margin-left: 5px"  color="success">
                          {{ message.message }}
                          <span style="font-size: 0.7em; margin-left: 3px"> <br> {{ message.time }}</span>
                        </v-chip>
                      </div>

                      <!--Other Messages-->
                      <div v-else-if="message.receiver !== 'all' && message.username !== 'Chatbot' && message.username !== userName">
                        <span style="font-weight: bold">{{ message.username }} @ {{ message.receiver }}</span>
                        <v-chip dark style="margin-left: 5px"  color="#c62828">
                          {{ message.message }}
                          <span style="font-size: 0.7em; margin-left: 3px"> <br> {{ message.time }}</span>
                        </v-chip>
                      </div>
                    </div>




                  </v-list-item>
                </v-list>
                <br>
                <div v-if="loggedIn && gifSelected" class="gif-container">
                  <img height="50" v-for="gif in gifs" :src="gif" :key="gif.id" @click="clickedOnGif(gif)">
                </div>
                <v-text-field color="primary" v-if="loggedIn && !gifSelected" :label="'Nachricht an: ' + this.receiver" dense outlined v-model="messageContent" @keyup.enter="sendMessage">
                  <template slot="prepend">
                    <v-btn v-if="gifSelected" icon @click="gifSelected = false">
                      <v-icon color="dynamic" left>mdi-chat-processing-outline</v-icon>
                    </v-btn>
                    <v-btn v-if="!gifSelected" icon @click="gifSelected = true">
                      <v-icon left>mdi-gif</v-icon>
                    </v-btn>
                  </template>

                  <template slot="append">
                    <v-btn v-if="!this.messageContent.length == 0" icon color="primary" style="margin-bottom: 10px;" @click="sendMessage">
                      <v-icon left>mdi-send-outline</v-icon>
                    </v-btn>
                  </template>
                </v-text-field>
                <v-text-field color="primary" v-if="loggedIn && gifSelected" label="GIF suchen" dense outlined v-model="searchTerm" @keyup.enter="getGifs">
                  <template slot="prepend">
                    <v-btn v-if="gifSelected" icon @click="gifSelected = false">
                      <v-icon color="dynamic" left>mdi-chat-processing-outline</v-icon>
                    </v-btn>
                    <v-btn v-if="!gifSelected" icon @click="gifSelected = true">
                      <v-icon left>mdi-gif</v-icon>
                    </v-btn>
                  </template>
                  <v-btn v-if="!this.messageContent.length == 0" icon color="primary" style="margin-bottom: 10px;" @click="sendMessage">
                    <v-icon left>mdi-send-outline</v-icon>
                  </v-btn>
                </v-text-field>
              </v-card-text>
            </v-card>

          </v-col>
        </v-row>
      </v-container>
      <v-snackbar v-model="welcomeSnack" color="success" :timeout= 3000 bottom>
        Willkommen im Chat, <span style="font-weight: bold">{{userName}}</span>!
        <v-btn color="black" text @click="welcomeSnack = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="bybySnack" color="error" :timeout= 3000 bottom>
        Bis bald!
        <v-btn color="black" text @click="bybySnack = false">Close</v-btn>
      </v-snackbar>
    </v-content>
  </v-app>
</template>

<script>
  import axios from "axios"


  // on fhnw server
  //const Url = 'http://10.35.148.180:8080'
  //const userUrl = Url + '/api/users'
  //const messageUrl = Url + '/api/messages'

  // local
  //const Url = 'http://127.0.0.1:5000'
  //const userUrl = Url + '/api/users'
  //const messageUrl = Url + '/api/messages'


  export default {
    name: 'App',
    components: {
    },
    data() {
      return {
        Url: 'http://127.0.0.1:5000',
        userUrl: 'http://127.0.0.1:5000/api/users',
        messageUrl: 'http://127.0.0.1:5000/api/messages',
        users: [], // Array of Strings with Usernames
        messages: [], // Array of Objects with actual Messages (username, message, time and receiver)
        userName: '',
        messageContent: '',
        loggedIn: false,
        serverConnected: false,
        chatbotMessages: true,
        dynamic: 'grey',
        welcomeSnack: false,
        bybySnack: false,
        receiver: 'all',
        refreshInterval: 5,
        password: null,
        showAllMessages: false,
        alert: false,
        searchTerm: "",
        gifs: [],
        gifSelected: false
      }
    },
    async created() {
      if (JSON.parse(localStorage.getItem('chat-app'))) {
        this.userName = JSON.parse(localStorage.getItem('chat-app')).userName
        this.loggedIn = JSON.parse(localStorage.getItem('chat-app')).loggedIn
      }
      this.getUsers();
      this.getMessages();
      this.updateData(this.refreshInterval * 1000);
    },
    computed: {
      filterAll: function() {
        let filtered = this.messages
        if (this.receiver === 'all') {
          filtered = filtered.filter(
                  m =>
                          m.receiver === 'all' ||
                          m.receiver === this.userName

          );
        }
        return filtered;
      },
      filterPrivate: function() {
        let filtered = this.messages
        if (this.receiver !== 'all') {
          filtered = filtered.filter(
                  m =>
                          // Nachrichten von Absender an mich
                          m.receiver === this.receiver &&
                          m.username === this.userName ||

                          m.receiver === this.userName &&
                          m.username === this.receiver
          );
        }
        return filtered;
      }
    },
    methods: {
      clickedOnGif (url) {
        this.messageContent = url
        this.sendMessage()
        this.gifSelected = false
      },
      getGifs() {
        let apiKey = "DA0U9E2wmRjm6XzJs5dDryacvuXxkRSg";
        let searchEndPoint = "https://api.giphy.com/v1/gifs/search?";
        let limit = 15;
        let url = `${searchEndPoint}&api_key=${apiKey}&q=${
                this.searchTerm
        }&limit=${limit}`;
        fetch(url)
                .then(response => {
                  return response.json();
                })
                .then(json => {
                  this.buildGifs(json);
                })
                .catch(err => console.log(err));
      },
      buildGifs(json) {
        this.gifs = json.data.map(gif => gif.id).map(gifId => {
          return `https://media.giphy.com/media/${gifId}/giphy.gif`;
        })
      },

      openSwaggerSite () {
        window.open(this.Url)
      },

      calcPrivateMessages () {
        let result = this.messages
        return result
      },
      // Method to fetch Userlist and Messages every x second
      updateData(interval) {
        setInterval(() => {
          this.getUsers()
          if (this.loggedIn) {
            this.getMessages()
          }
        }, interval)
      },
      // Fetches the logged in Users from Backend
      async getUsers() {
        try {
          const users = await axios.get(this.userUrl);
          this.users = users.data;
          this.serverConnected = true;
          if (this.userName === 'admin' && this.loggedIn) {
            this.dynamic = '#c62828';
          }else {
            this.dynamic = '#546e7a';
          }
        } catch(e) {
          console.error(e)
          this.serverConnected = false;
          this.dynamic = 'grey';
        }
      },
      // Fetches theMessages from Backend
      async getMessages() {
          try {
            const mes = await axios.get(this.messageUrl);
            this.messages = mes.data;
          } catch(e) {
            console.error(e)
          }
      },
      checkAdmin () {
        if (this.userName === 'admin') {
          if (this.password === 'kvanc2020') {
            this.signIn()
          }else {
            this.alert = true
            setTimeout(() => {
              this.alert = false
            }, 1000);
          }
        }else {
          this.signIn()
        }
      },
      // addd the User to The Userlist in Backend
      async signIn() {
        try {
          const res = await axios.put(this.userUrl, {username: this.userName});
          this.users = [...this.users, res.data];
          this.$store.commit('setLoggedInStatus', true )
          this.$store.commit('setUserName', this.userName )
          this.loggedIn = true;
          this.getUsers();
          this.sendChatboxMessage(' hat sich angemeldet');
          this.welcomeSnack = true;
        } catch(e) {
          console.error(e)
        }
      },

      // Removes User from the List
      async signOut() {
        try {
          await axios.delete(this.userUrl, {data: {username: this.userName}});
          this.bybySnack = true;
          this.sendChatboxMessage(' hat sich abgemeldet');
          this.getUsers();
          this.$store.commit('setLoggedInStatus', false )
          this.$store.commit('setUserName', '' )
          this.loggedIn = false;
          this.userName = '';
        } catch(e) {
          console.error(e)
        }
      },
      // Gets the Actual Time in Format (HH:MM)
      getTime() {
        let time = new Date().toJSON().slice(11,19).replace(/-/g,'/');
        return time.toString();
      },
      // Adds a Message to the List with the actual Username
      async sendMessage() {
          try {
            const res = await axios.post(this.messageUrl, {username: this.userName, message: this.messageContent, time: this.getTime(), receiver: this.receiver})
            this.messages = [...this.messages, res.data]
            this.messageContent = ''
            this.getMessages()
          } catch(e) {
            console.error(e)
          }
      },
      // Adds a Message to the List with the actual Username
      async sendChatboxMessage(mes) {
        try {
          const res = await axios.post(this.messageUrl, {username: 'Chatbot', message: this.userName + mes, time: this.getTime(), receiver: 'all'});
          this.messages = [...this.messages, res.data];
          this.getMessages();
        } catch(e) {
          console.error(e)
        }
      },
      changeChatbotStatus() {
        this.chatbotMessages =! this.chatbotMessages;
        this.getMessages();
      }
    },

  }
</script>

<style>
  .switch-center {
    display: flex;
    justify-content: center;
  }
</style>