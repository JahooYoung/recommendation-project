<template>
  <b-nav-form>
    <type-ahead
      v-model="query"
      :placeholder="$t('Search events...')"
      :no-result-text="$t('No result.')"
      :searching-text="$t('Just a moment...')"
      select-first
      :min-chars="1"
      :delay-time="250"
      :fetch="fetch"
      :get-response="getResponse"
      :highlighting="highlighting"
      :on-hit="onHit"
      class="mr-sm-2"
      style="width: 20em"
    />
  </b-nav-form>
</template>

<script>
import { BNavForm } from 'bootstrap-vue'
import algoliasearch from 'algoliasearch/lite'
import TypeAhead from './TypeAhead.vue'

export default {
  name: 'SearchBox',
  components: {
    TypeAhead,
    BNavForm
  },
  data () {
    return {
      query: '',
      index: algoliasearch(
        'WN4Q0PFNA4',
        '856d81f42e715a208a22112291343573'
      ).initIndex('event_index')
    }
  },
  methods: {
    fetch () {
      return this.index.search({
        query: this.query,
        attributesToSnippet: ['description'],
        snippetEllipsisText: '...'
      })
    },
    getResponse (content) {
      return content.hits
    },
    replaceTag (value) {
      return value
        .replace(/<em>/g, `<span class="search-highlight">`)
        .replace(/<\/em>/g, `</span>`)
    },
    highlighting (item) {
      const title = this.replaceTag(item._highlightResult.title.value)
      return `<h6><b>${title}</b></h6><small>Short description?</small>`
      // const description = this.replaceTag(item._snippetResult.description.value)
      // return `<h5>${title}</h5>${description}`
    },
    onHit (item, self, id) {
      if (id !== undefined) {
        this.$router.push(`/event/${item.id}`)
      }
    }
  }
}
</script>

<style>
.search-highlight {
  color: #2196F3
}
</style>
