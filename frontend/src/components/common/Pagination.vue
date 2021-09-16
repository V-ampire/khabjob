<template>
  <b-pagination
    v-model="currentPage"
    :per-page="perPage"
    :total-rows="count"
    align="center"
    v-on:page-click="pageChange"
  ></b-pagination>
</template>

<script>
import { ON_PAGINATE } from '@/events/types' 

export default {
  props: {
    count: Number,
    perPage: {
      type: Number,
      default: 20
    },
  },
  data () {
    return {
      currentPage: 1
    }
  },
  methods: {
    pageChange(event, page) {
      console.log(page)
      this.currentPage = page
      this.$emit(ON_PAGINATE, page)
    }
  },
}
</script>