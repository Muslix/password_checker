<!-- src/components/PasswordChecker.vue -->

<template>
  <div>
    <h1>Passwortprüfung</h1>
    <input v-model="password" type="password" placeholder="Geben Sie Ihr Passwort ein" />
    <button @click="checkPassword">Überprüfen</button>
    <p v-if="status === 'unsafe'">Ihr Passwort befindet sich in der Liste.</p>
    <p v-if="status === 'safe'">Ihr Passwort ist sicher (nicht in der Liste).</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      password: '',
      status: null,
    };
  },
  methods: {
    async checkPassword() {
      const response = await fetch('http://localhost:5000/check_password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: this.password }),
      });
      const result = await response.json();
      this.status = result.status;
    },
  },
};
</script>
