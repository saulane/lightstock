<template>
    <div v-if="isLoading" class="loading-screen">
        <p>
            Loading
            <span class="point-anim point-1">.</span>
            <span class="point-anim point-2">.</span>
            <span class="point-anim point-3">.</span>
        </p>
    </div>
</template>

<script>
import { useStore } from 'vuex';
import { computed } from 'vue';


export default({
    setup(){
        const store = useStore()

        return{
            isLoading: computed(() => store.state.isLoading),
        };
    }
})
</script>