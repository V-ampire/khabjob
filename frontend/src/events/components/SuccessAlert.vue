<template>
    <v-snackbar
      v-model="showAlert"
      color="success"
      top
    >
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn
          color="success"
          x-small
          fab
          v-bind="attrs"
          @click="close()"
        >
         <v-icon color="white">fa-times</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
</template>

<script>
import utils from '@/core/services/events/utils';
import alertMixin from '@/core/mixins/alertMixin';

export default {
  mixins: [alertMixin],
  
  mounted: function() {
    utils.onSuccessEvent(this.open);
  },
}
</script>