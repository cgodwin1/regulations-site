<template>
    <div v-bind:class="{ visible: visible }">
        <button v-on:click="click">{{ buttonText }}</button>
    </div>
</template>

<script>
export default {
    name: "collapse-button",

    created: function() {
        this.visible = this.state === "expanded";
        this.$root.$on("collapse-toggle", this.toggle);
    },

    props: {
        name: {
            type: String,
            required: true,
        },
        state: { //expanded or collapsed
            type: String,
            required: true,
        },
        expanded_text: {
            type: String,
            required: false,
            default: "Hide",
        },
        collapsed_text: {
            type: String,
            required: false,
            default: "Show",
        },
    },

    computed: {
        buttonText: function() {
            return this.visible ? this.expanded_text : this.collapsed_text;
        },
    },

    data: function() {
        return {
            visible: true,
        }
    },

    methods: {
        click: function(event) {
            this.$root.$emit("collapse-toggle", this.name);
        },
        toggle: function(target) {
            if(this.name === target) {
                this.visible = !this.visible;
            }
        },
    },
};
</script>
