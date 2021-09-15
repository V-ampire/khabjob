export default {
  data() {
    return {
      showAlert: false,
      message: '',
      timeout: 5000
    }
  },
  methods: {
    open (message) {
      this.message = message;
      this.showAlert = true;
    },
    close () {
      this.showAlert = false;
    }
  },
}