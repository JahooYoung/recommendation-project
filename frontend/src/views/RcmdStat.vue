<template>
  <b-container>
    <div align="center">
      <h2> Recommendation Statistics </h2>
    </div>
    <b-row>
      <b-col
        cols="12"
        md="4"
        class="px-0 my-3"
      >
        <b-input-group>
          <b-form-input
            v-model="filter"
            :placeholder="$t(`Search `) + `${itemName}`"
            debounce="500"
          />
          <b-input-group-append>
            <b-button
              size="sm"
              :disabled="!filter"
              @click="filter = ''"
            >
              {{ $t('Clear') }}
            </b-button>
          </b-input-group-append>
        </b-input-group>
      </b-col>
      <b-col
        cols="12"
        md="8"
        class="px-0 my-3"
        align="right"
      >
        <!-- <slot name="buttons" /> -->

        <b-button
          variant="outline-dark"
          pill
          @click="$refs['rcmd-stat-table'].refresh()"
        >
          {{ $t('Refresh') }}
        </b-button>
      </b-col>

      <b-table
        ref="rcmd-stat-table"
        striped
        hover
        show-empty
        responsive
        :busy.sync="isBusy"
        :filter="filter"
        :per-page="perPage"
        :current-page="currentPage"
        :empty-text="$t('There are no records to show')"
        :empty-filtered-text="$t('There are no records matching your request')"
        :items="provider"
        :fields="fields"
        primary-key="timestamp"
      >
        <template #table-busy>
          <div class="text-center text-primary my-2">
            <b-spinner class="align-middle mr-2" />
            <strong>{{ $t('Loading...') }}</strong>
          </div>
        </template>
      </b-table>

      <b-col cols="12">
        <div class="mt-3">
          <b-pagination
            v-model="currentPage"
            :total-rows="totalRows"
            :per-page="perPage"
            limit="9"
            align="center"
            aria-controls="rcmd-stat-table"
          />
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { snakeCase } from '@/plugins/axios'

export default {
  name: 'RcmdStat',
  data() {
    return {
      isBusy: false,
      perPage: 10,
      currentPage: 1,
      itemName: 'rcmd-stat',
      totalRows: 0,
      filter: '',
      fields: [
        {
          key: 'timestamp',
          formatter: t => (new Date(t * 1000)).toLocaleString(),
          sortable: true
        },
        {
          key: 'rcmdClickNum',
          label: 'Number of Recommendation Clicks In 5 Minutes',
          sortable: true
        },
        // { key: 'owner', sortable: true, formatter: x => x.username },
        // { key: 'created', sortable: true, formatter: t => t.toLocaleString() },
        // { key: 'lastModified', sortable: true, formatter: t => t.toLocaleString() },
      ]
    }
  },
  methods: {
    async provider(ctx) {
      try {
        const res = await this.axios.get(`/api/rcmd-stats/`, {
          params: {
            limit: ctx.perPage,
            offset: ctx.perPage * (ctx.currentPage - 1),
            search: ctx.filter,
            ordering: (ctx.sortDesc ? '-' : '') + snakeCase(ctx.sortBy)
          }
        })
        this.totalRows = res.data.count
        return res.data.results
      } catch (err) {
        console.log(err)
        return []
      }
    },
  }
}
</script>
