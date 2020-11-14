<template>
  <b-sidebar
    :id="id"
    title="Table of Contents"
    shadow
  >
    <div class="px-3 py-2">
      <div
        v-for="link in toc"
        :key="link.slug"
        :class="'toc-header-' + link.lvl"
      >
        <b-link
          :href="`#${link.slug}`"
        >
          {{ link.content }}
        </b-link>
      </div>
    </div>
  </b-sidebar>
</template>

<script>


export default {
  name: 'TOCSidebar',
  props: {
    id: String,
    toc: Array
  },
}
</script>

<style>
.toc-header-1 {
  text-indent: 0rem;
}
.toc-header-2 {
  text-indent: 1rem;
}
.toc-header-3 {
  text-indent: 2rem;
}
.toc-header-4 {
  text-indent: 3rem;
}
.toc-header-5 {
  text-indent: 4rem;
}
.toc-header-6 {
  text-indent: 5rem;
}
</style>
