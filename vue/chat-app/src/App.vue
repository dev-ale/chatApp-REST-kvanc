<template>
  <v-app>

    <v-app-bar app dark :color="dynamic">
      <v-spacer></v-spacer>
      <v-toolbar-title>ChatApp REST - kvanc 2020</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-chip v-if="serverConnected" style="margin-left: 5px" color="success" @click="snackbar = true">connected</v-chip>
      <v-chip v-if="!serverConnected" style="margin-left: 5px" color="error">offline</v-chip>
      <v-snackbar v-model="welcomeSnack" color="success" :timeout= 3000 bottom>
        Willkommen im Chat, <span style="font-weight: bold">{{ userName }}</span>!
        <v-btn color="black" text @click="welcomeSnack = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="bybySnack" color="error" :timeout= 3000 bottom>
        Bis bald!
        <v-btn color="black" text @click="bybySnack = false">Close</v-btn>
      </v-snackbar>
    </v-app-bar>



    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="3">
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
                  <v-text-field v-if="!loggedIn" label="Benutzername" outlined dense v-model="userName" @keyup.enter="signIn">
                    <template slot="append">
                      <v-btn icon color="dynamic" style="margin-bottom: 10px;" @click="signIn">
                        <v-icon left>mdi-login-variant</v-icon>
                      </v-btn>
                    </template>
                  </v-text-field>
                  <v-list >
                    <v-list-item v-for="user of users" :key="user.ip">
                      <v-icon>mdi-account</v-icon>
                      <span style="font-weight: bold; font-size: 1.2em;"> {{ user.username }} </span> : {{ user.ip }}
                      <v-btn depressed x-small color="error" style="margin-left: 5px" v-if="user.username === userName" @click="signOut">Logout</v-btn>
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
            <v-card v-if="loggedIn && serverConnected" class="elevation-12">
              <v-toolbar :color="dynamic" dark flat>
                <v-toolbar-title>Chat</v-toolbar-title>
                <v-spacer/>
                  <!--TODO: Switch to turn of and on Chatbot Messages doesnt work yet-->
                  <!--<v-switch label="Chatbot" @change="changeChatbotStatus"></v-switch>-->
              </v-toolbar>
              <v-card-text>
                <p v-if="this.messages.length < 1">Keine Nachrichten</p>
                <v-list>
                  <v-list-item v-for="message of messages" :key="message.time">

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



                  </v-list-item>
                </v-list>
                <br>
                <v-text-field color="primary" v-if="loggedIn" label="Nachricht" dense outlined v-model="messageContent" @keyup.enter="sendMessage">
                  <template slot="append">
                    <v-btn v-if="!this.messageContent.length == 0" icon color="primary" style="margin-bottom: 10px;" @click="sendMessage">
                      <v-icon left>mdi-send-outline</v-icon>
                    </v-btn>
                  </template>
                </v-text-field>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  import axios from "axios"

   const userUrl = 'http://127.0.0.1:5000/api/users';
   const messageUrl = 'http://127.0.0.1:5000/api/messages';

  export default {
    name: 'App',
    components: {
    },
    data() {
      return {
        users: [], // Array of Objects with actual Users (ip, username)
        messages: [], // Array of Objects with actual Messages (username, message)
        userName: '',
        ip: '',
        messageContent: '',
        loggedIn: false,
        serverConnected: false,
        chatbotMessages: true,
        dynamic: 'grey',
        welcomeSnack: false,
        bybySnack: false
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
          this.serverConnected = true;
          this.dynamic = '#546e7a';
        } catch(e) {
          console.error(e)
          this.serverConnected = false;
          this.dynamic = 'grey';
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
          this.sendChatboxMessage(' hat sich angemeldet');
          this.welcomeSnack = true;
        } catch(e) {
          console.error(e)
        }
      },

      // Removes User from the List
      async signOut() {
        try {
          console.log(this.userName + this.ip);
          await axios.delete(userUrl, {data: {username: this.userName, ip: this.ip}});
          this.bybySnack = true;
          this.sendChatboxMessage(' hat sich abgemeldet');
          this.getUsers();
          this.loggedIn = false;
          this.userName = '';
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
      async sendMessage() {
        try {
          const res = await axios.post(messageUrl, {username: this.userName, message: this.messageContent, time: this.getTime()});
          this.messages = [...this.messages, res.data];
          this.messageContent = '';
          this.getMessages();
        } catch(e) {
          console.error(e)
        }
      },
      // Adds a Message to the List with the actual Username
      async sendChatboxMessage(mes) {
        try {
          const res = await axios.post(messageUrl, {username: 'Chatbot', message: this.userName + mes, time: this.getTime()});
          this.messages = [...this.messages, res.data];
          this.getMessages();
        } catch(e) {
          console.error(e)
        }
      },
      changeChatbotStatus() {
        this.chatbotMessages =! this.chatbotMessages;
        this.getMessages();
        console.log(this.chatbotMessages)
      }
    },

  }
</script>
