import RelatedRules from './RelatedRules.js';
import VerticalCollapsible from './VerticalCollapsible.js';
import CollapseButton from './CollapseButton.js';
import Vue from "../../node_modules/vue/dist/vue.esm.browser.min.js";

function makeStateful(el) {
    const state_change_target = el.getAttribute("data-state-name");
    const state_change_buttons = document.querySelectorAll(`[data-set-state][data-state-name='${state_change_target}']`);

    for (const state_change_button of state_change_buttons) {
        state_change_button.addEventListener('click', function() {
            const state = this.getAttribute("data-set-state");
            el.setAttribute("data-state", state);
        });
    }
}

function main() {
    const stateful_elements = document.querySelectorAll("[data-state]")

    for (const el of stateful_elements) {
        makeStateful(el);
    }

    
    new Vue({
        components: {
            RelatedRules,
            VerticalCollapsible,
            CollapseButton,
        }
    }).$mount("#vue-app")
}

main();
