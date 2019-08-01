<template>
  <div class="no-video">
    <div class="no-video-inner">
      <font-awesome-icon icon="video-slash" />
      无视频
    </div>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 16 9"
      version="1.1"
      class="no-video-placeholder"
    >
      <!---->
    </svg>
  </div>
</template>

<script>
export default {
  name: 'NoVideoPlaceholder'
}
</script>

<style scoped>
  .no-video {
    position: relative;
    background: rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    user-select: none;
    pointer-events: none;
  }

  .no-video-placeholder {
    width: 100%;
  }

  .no-video-inner {
    position: absolute;
    color: rgba(0, 0, 0, 0.5);
  }
</style>