<template>
	<div class="flex items-center justify-center w-full h-full">
		<label
			for="dropzone-file"
			class="flex flex-col items-center justify-center w-full lg:h-full h-[300px] border-2 border-dashed rounded-lg"
			:class="{
				'border-blue-500 bg-blue-50': file !== null,
				'border-gray-300 bg-gray-50 cursor-pointer': file === null,
			}"
		>
			<div
				class="flex flex-col items-center justify-center"
				v-if="file === null"
			>
				<svg
					class="w-8 h-8 mb-4 text-gray-500"
					aria-hidden="true"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 20 16"
				>
					<path
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
					/>
				</svg>
				<p class="mb-2 text-sm text-gray-500">
					<span class="font-semibold">Click to upload</span> or drag and drop
				</p>
				<p class="text-xs text-gray-500">Network traffic file (.pacap)</p>
			</div>
			<div class="flex flex-col items-center justify-center" v-else>
				<svg
					class="w-8 h-8 mb-4 text-blue-500"
					aria-hidden="true"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
				>
					<path
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M5 13l4 4L19 7"
					/>
				</svg>
				<p class="mb-2 text-sm text-gray-800">
					<span class="font-semibold">{{ file.name }}</span>
				</p>
				<p class="text-xs text-gray-500 mb-6">{{ file.size }} bytes</p>
				<div class="flex gap-2 items-center">
					<button
						type="button"
						class="flex items-center justify-center text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-8 py-2.5 text-center disabled:opacity-50 disabled:pointer-events-none"
						@click="analyseTraffic"
						:disabled="loading"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
							fill="currentColor"
							class="animate-spin w-5 h-5 mx-10"
							v-if="loading"
						>
							<path
								d="M18.364 5.63604L16.9497 7.05025C15.683 5.7835 13.933 5 12 5C8.13401 5 5 8.13401 5 12C5 15.866 8.13401 19 12 19C15.866 19 19 15.866 19 12H21C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C14.4853 3 16.7353 4.00736 18.364 5.63604Z"
							></path>
						</svg>
						<span v-else> Analyse Traffic </span>
					</button>
					<button
						type="button"
						class="h-[35px] w-[35px] flex items-center justify-center text-white bg-red-700 hover:bg-red-800 focus:outline-none focus:ring-4 focus:ring-red-300 font-medium rounded-full text-sm"
						@click.prevent="cancelAnalysis"
						title="Cancel analysis"
						v-if="!loading"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
							fill="currentColor"
							class="w-5 h-5"
						>
							<path
								d="M6 18L18 6M6 6l12 12"
								stroke="currentColor"
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
							></path>
						</svg>
					</button>
				</div>
			</div>
			<input
				id="dropzone-file"
				type="file"
				class="hidden"
				accept=".pcap"
				@change="handleFileChange"
				:disabled="file !== null"
			/>
		</label>
	</div>
</template>

<script>
export default {
	name: "UploadPcap",
	data() {
		return {
			file: null,
			loading: false,
		};
	},
	methods: {
		handleFileChange(e) {
			if (e.target.files.length) this.file = e.target.files[0];
		},
		async analyseTraffic() {
			this.loading = true;

			// Send the file to the server for analysis
			const formData = new FormData();
			formData.append("file", this.file);
			const response = await fetch("http://127.0.0.1:8000/detect", {
				method: "POST",
				body: formData,
			});

			// Get the analysis results
			const analysis = await response.json();
			this.$emit("analysis-finished", analysis.data);

			this.loading = false;
		},
		cancelAnalysis() {
			if (confirm("Are you sure ?")) {
				this.file = null;
				this.$emit("analysis-finished", []);
			}
		},
	},
};
</script>
