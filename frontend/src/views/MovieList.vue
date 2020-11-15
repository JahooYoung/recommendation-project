<template>
  <b-container>
    <div align="center">
      <h2> All Movies </h2>
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
          @click="$refs['movie-table'].refresh()"
        >
          {{ $t('Refresh') }}
        </b-button>
      </b-col>

      <b-table
        ref="movie-table"
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
        primary-key="id"
        @row-clicked="toggleItemDetails"
      >
        <template #table-busy>
          <div class="text-center text-primary my-2">
            <b-spinner class="align-middle mr-2" />
            <strong>{{ $t('Loading...') }}</strong>
          </div>
        </template>

        <template #cell(title)="row">
          <b-link :to="`/movies/${row.item.id}`">
            {{ row.value }}
          </b-link>
        </template>

        <template #cell(genres)="row">
          <b-badge
            v-for="gr in row.value.split('|')"
            :key="`${row.item.id}-${gr}`"
            pill
            variant="dark"
            class="mx-1"
            @click="filter = gr"
          >
            {{ gr }}
          </b-badge>
        </template>

        <template #cell(meanRating)="row">
          <b-form-rating
            :value="row.value"
            inline
            readonly
          />
        </template>

        <template #cell(imdbId)="row">
          <b-link
            :href="`https://www.imdb.com/title/tt${String(row.value).padStart(7, '0')}/`"
            target="_blank"
          >
            {{ row.value }}
          </b-link>
        </template>

        <template #row-details="row">
          <b-form-group
            label="Your Rating: "
            label-cols="2"
          >
            <b-form-rating
              :value="row.item.rating.rating || 0"
              inline
              @change="row.item.updateRating"
            />
          </b-form-group>
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
            aria-controls="movie-table"
          />
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { snakeCase } from '@/plugins/axios'

export default {
  name: 'MovieList',
  data() {
    return {
      isBusy: false,
      perPage: 10,
      currentPage: 1,
      itemName: 'movie',
      totalRows: 0,
      filter: '',
      fields: [
        { key: 'id', sortable: true },
        { key: 'title' },
        { key: 'genres' },
        { key: 'meanRating', sortable: true },
        { key: 'imdbId', sortable: true },
        // { key: 'owner', sortable: true, formatter: x => x.username },
        // { key: 'created', sortable: true, formatter: t => t.toLocaleString() },
        // { key: 'lastModified', sortable: true, formatter: t => t.toLocaleString() },
      ]
    }
  },
  methods: {
    async provider(ctx) {
      try {
        const res = await this.axios.get(`/api/movies/`, {
          params: {
            limit: ctx.perPage,
            offset: ctx.perPage * (ctx.currentPage - 1),
            search: ctx.filter,
            ordering: (ctx.sortDesc ? '-' : '') + snakeCase(ctx.sortBy)
          }
        })
        this.totalRows = res.data.count
        const movies = res.data.results.map(movie => {
          movie._showDetails = false
          return movie
        })
        return movies
      } catch (err) {
        console.log(err)
        return []
      }
    },
    async toggleItemDetails(item, index, event) {
      if (item._showDetails) {
        item._showDetails = false
        return
      }
      await this.needLogin()
      try {
        const res = await this.axios.get(`/api/movies/${item.id}/`)
        item.rating = res.data.rating || { rating: 0 }
        this.isBusy = false
        item.updateRating = async (newRating) => {
          // console.log(item, newRating)
          this.isBusy = true
          try {
            if (item.rating.id === undefined) {
              const res = await this.axios.post(`/api/ratings/`, {
                rating: newRating,
                movie: item.id
              })
              item.rating = res.data
            } else {
              const res = await this.axios.patch(`/api/ratings/${item.rating.id}/`, {
                rating: newRating
              })
              item.rating = res.data
            }
          } catch (err) {
            console.log(err)
          }
          this.isBusy = false
        }
      } catch (err) {
        console.log(err)
      }
      item._showDetails = true
    },
  }
}
</script>
