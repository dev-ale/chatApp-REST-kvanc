<template>
    <h3>Chat:</h3>
    <p v-if="this.messages.length < 1">Keine Nachrichten, bis jetzt...</p>
    <ul>
        <li v-for="message of messages" :key="message.message"><span style="font-weight: bold">{{ message.username }}</span> : {{ message.message }} </li>
    </ul>
    <div>
        <input placeholder="message" v-if="!loggedIn" type="text" v-model="userName" @keyup.enter="sendMessage">
    </div>
</template>

<script>
    import axios from "axios"

    const messageUrl = 'http://127.0.0.1:5000/api/messages';

    export default {
        name: 'chat',
        data () {
            return {
                messages: []
            }
        },
        async created() {
            try {
                const mes = await axios.get(messageUrl);
                this.messages = mes.data;
            } catch(e) {
                console.error(e)
            }
        },methods: {
            async sendMessage() {
                try {
                    const res = await axios.put(messageUrl, {username: this.userName, message: this.message});

                    this.messages = [...this.messages, res.data];
                    this.message = '';
                    window.location.reload();
                } catch(e) {
                    console.error(e)
                }
            },
        },

    }
</script>

