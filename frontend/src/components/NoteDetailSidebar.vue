<template>
  <b-sidebar
    :id="id"
    title="Note Detail"
    shadow
  >
    <div class="px-3 py-2" v-if="document">
      <h5>Title</h5>
      <p>
        {{ document.title }}
      </p>
      <h5>Author</h5>
      <p>{{ document.owner.username }}</p>
      <h5>Create Time</h5>
      <p>{{ document.created.toLocaleString() }}</p>
      <h5>Last Modified Time</h5>
      <p>{{ document.lastModified.toLocaleString() }}</p>
      <h5 v-if="document.lastSync">Last Sync Time</h5>
      <p v-if="document.lastSync">{{ document.lastSync.toLocaleString() }}</p>
    </div>
  </b-sidebar>
</template>

<script>


export default {
  name: 'NoteDetailSidebar',
  props: {
    id: String,
    // ['url', 'id', 'title', 'owner', 'body', 'created', 'last_modified']
    document: Object
  }
}
</script>

<style>

</style>
