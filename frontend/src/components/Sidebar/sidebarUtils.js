import { ref, computed } from 'vue';

export const collapsed = ref(true)
export const toggleSidebar = () => (collapsed.value = !collapsed.value)

export const SIDEBAR_WIDTH = ref(320);
export const SIDEBAR_WIDTH_COLLAPSED = ref(96);

export const sidebarWidth = computed(() => {
  resizeSidebar();
  return `${collapsed.value ? SIDEBAR_WIDTH_COLLAPSED.value : SIDEBAR_WIDTH.value}px`
});

export const resizeSidebar = () => {
  if (window.innerWidth > 768) {
    SIDEBAR_WIDTH.value = 320;
    SIDEBAR_WIDTH_COLLAPSED.value = 96;
  } else if (window.innerWidth <= 768) {
    SIDEBAR_WIDTH.value = 210;
    SIDEBAR_WIDTH_COLLAPSED.value = 72
  };
};