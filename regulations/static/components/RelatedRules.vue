<template>
    <div>
        <related-rule-list :rules="rules"></related-rule-list>
    </div>
</template>

<script>
import RelatedRuleList from './RelatedRuleList.vue'
export default {
    components: {
        RelatedRuleList,
    },

    props: {
        title: {
            type: String,
            required: true,
        },
        part: {
            type: String,
            required: true,
        },
        limit: {
            type: Number,
            default: 3,
        },
    },

    data() {
        return {
            rules: null,
        }
    },

    async created() {
        this.rules = await this.fetch_rules(this.title, this.part, this.limit);
    },

    methods: {
        async fetch_rules(title, part, limit) {
            const response = await fetch(`https://www.federalregister.gov/api/v1/documents.json?fields[]=type&fields[]=abstract&fields[]=citation&fields[]=correction_of&fields[]=dates&fields[]=docket_id&fields[]=docket_ids&fields[]=document_number&fields[]=effective_on&fields[]=html_url&fields[]=publication_date&fields[]=regulation_id_number_info&fields[]=regulation_id_numbers&fields[]=title&order=newest&conditions[type][]=RULE&conditions[cfr][title]=${title}&conditions[cfr][part]=${part}&per_page=${limit}`);
            const rules = await response.json();
            const by_effective_on = (a,b) => {
              return new Date(b.effective_on) - new Date(a.effective_on);
            };
            return rules.results.sort(by_effective_on);
        }
    }
};
</script>
