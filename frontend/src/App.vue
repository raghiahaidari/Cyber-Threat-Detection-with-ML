<template>
	<div>
		<Header />
		<div class="container mx-auto py-10">
			<div
				class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start lg:h-[450px]"
			>
				<UploadPcap @analysis-finished="setResults" />
				<PreviewResults :frames="results" />
			</div>
		</div>
	</div>
</template>

<script>
import Header from "./components/Header.vue";
import UploadPcap from "./components/UploadPcap.vue";
import PreviewResults from "./components/PreviewResults.vue";

export default {
	components: {
		Header,
		UploadPcap,
		PreviewResults,
	},
	data() {
		return {
			results: [],
		};
	},
	methods: {
		setResults(analysis) {
			this.results = analysis;
		},
	},
};
</script>
