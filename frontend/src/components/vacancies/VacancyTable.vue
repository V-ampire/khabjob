<template>
  <div class="vacancies-table">
    <b-form-checkbox-group
        id="choices"
        v-model="selected"
      >
    <b-table
      striped 
      hover 
      :items="vacancyList" 
      :fields="fields"
    > 
      <template #cell(name)="data">
        <router-link class="table-link" :to="{ name: 'AdminVacancyDetail', params: { vacancyId: data.item.id }}">
          {{ data.item.name }}
        </router-link>
      </template>
      <template #cell(source)="data">
        <a class="table-link" target="blank" :href="data.item.source">{{ data.item.source }}</a>
      </template>
      <template #cell(source_name)="data">
        <b-badge 
          class="mr-1" 
          pill 
          :variant="data.item.source_name"
        >{{ data.item.source_name }}</b-badge>
      </template>
      <template #cell(is_published)="data">
        <font-awesome-icon icon="check-circle" v-if="data.item.is_published" class="text-success" />
        <font-awesome-icon icon="times-circle" v-else class="text-danger" />
      </template>
      <template #head(id)>
        <b-form-checkbox-group>
          <b-form-checkbox v-model="selectAll" v-on:change="toggleAll"></b-form-checkbox>
        </b-form-checkbox-group>
      </template>
      <template #cell(id)="data">
        <b-form-checkbox :value="data.item.id" v-on:change="select"></b-form-checkbox>
      </template>
    </b-table>
    </b-form-checkbox-group>
    <Pagination 
      :count="count"
      :perPage="perPage"
      v-on:onPaginate="paginate"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Pagination from '@/components/common/Pagination.vue'
import { ON_PAGINATE } from '@/events/types' 

export default {
  components: {
    Pagination,
  },
  props: {
    perPage: {
      type: Number,
      default: 20
    },
  },
  data() {
    return {
      fields: [
        {
          key: 'name',
          label: 'Название вакансии',
          sortable: true
        },
        {
          key: 'source',
          label: 'Ссылка',
          sortable: true
        },
        {
          key: 'source_name',
          label: 'Источник',
          sortable: true,
        },
        {
          key: 'modified_at',
          label: 'Дата обновления',
          sortable: true,
        },
        {
          key: 'is_published',
          label: 'Статус публикации',
          sortable: true,
        },
        {
          key: 'id',
          sortable: false,
        }
      ],
      selectAll: [],
      selected: []
    }
  },
  computed: {
    ...mapState('vacancies', [
      'vacancyList',
      'count',
    ]),
  },
  methods: {
    paginate(page) {
      this.selectAll = []
      this.selected = []
      this.$emit(ON_PAGINATE, page)
    },
    toggleAll() {
      if (this.selectAll.length > 0) {
        for (let vacancy of this.vacancyList) {
          this.selected.push(vacancy.id)
        }
      } else {
        this.selected = []
      }
    },
    select() {
      this.selectAll = []
    },
    getSelectedIds() {
      return this.selected
    },
    clearSelected() {
      this.selected = []
    }
  },
}
</script>


<style>
  .table-link {
    text-decoration: underline;
  }
</style>