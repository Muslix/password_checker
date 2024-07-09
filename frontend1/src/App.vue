<!-- src/App.vue -->

<template>
  <div id="app">
    <PasswordChecker />
  </div>
</template>

<script>
import PasswordChecker from './components/PasswordChecker.vue';

export default {
  name: 'App',
  components: {
    PasswordChecker,
  },
};
</script>
