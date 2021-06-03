<template>
    <div class="collapse-button" v-bind:class="{ collapsed: collapsed }">
        <button v-on:click="click">Press</button>
    </div>
</template>

<script>
export default {
    name: 'collapse-button',

    components: {

    },

    created: function() {
        this.$root.$on("collapse-toggle", this.toggle);
    },

    props: {
        name: {
            type: String,
            required: true,
        },
        collapsed: {
            type: Boolean,
            required: true,
        },
    },

    computed: {

    },

    methods: {
        click: function(event) {
            this.$root.$emit("collapse-toggle", this.name);
        },
        toggle: function(target) {
            if(this.name === target) {
                this.collapsed = !this.collapsed;  
            }
        },
    },

    filters: {

    },
};
</script>
