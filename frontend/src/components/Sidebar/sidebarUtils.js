import { ref, computed } from 'vue';

export const collapsed = ref(true)
export const toggleSidebar = () => (collapsed.value = !collapsed.value)

export const SIDEBAR_WIDTH = ref(280);
export const SIDEBAR_WIDTH_COLLAPSED = ref(96);

export const sidebarWidth = computed(() => {
  resizeSidebar();
  return `${collapsed.value ? SIDEBAR_WIDTH_COLLAPSED.value : SIDEBAR_WIDTH.value}px`
});

export const resizeSidebar = () => {
  if (window.innerWidth > 1169) {
    SIDEBAR_WIDTH.value = 280;
    SIDEBAR_WIDTH_COLLAPSED.value = 96;
  } else if (window.innerWidth <= 1169 && window.innerWidth >= 768) {
    SIDEBAR_WIDTH.value = 210;
    SIDEBAR_WIDTH_COLLAPSED.value = 72;
  } else {
    SIDEBAR_WIDTH.value = 148;
    SIDEBAR_WIDTH_COLLAPSED.value = 44;
  }
};
