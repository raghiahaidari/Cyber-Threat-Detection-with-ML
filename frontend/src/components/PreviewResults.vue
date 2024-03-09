<template>
	<div
		class="relative w-full lg:h-full overflow-x-auto"
		v-if="frames && frames.length > 0"
	>
		<table class="w-full text-sm text-left text-gray-500">
			<thead class="text-sm text-gray-800 uppercase bg-white">
				<tr>
					<th scope="col" class="px-6 py-3">From</th>
					<th scope="col" class="px-6 py-3">To</th>
					<th scope="col" class="px-6 py-3">Range</th>
					<th scope="col" class="px-6 py-3">Status</th>
					<th scope="col" width="50px"></th>
				</tr>
			</thead>
			<tbody class="border">
				<tr
					v-for="(frame, index) in frames"
					:key="index"
					class="border"
					:class="{
						'bg-red-50 border-red-500': frame.status === 'ddos',
						'bg-green-50 border-green-500': frame.status === 'normal',
					}"
				>
					<td class="px-6 py-4 whitespace-nowrap">{{ frame.from }}</td>
					<td class="px-6 py-4 whitespace-nowrap">{{ frame.to }}</td>
					<td class="px-6 py-4 whitespace-nowrap">
						{{ frame.to - frame.from }} frames
					</td>
					<td class="px-6 py-4 whitespace-nowrap font-bold">
						{{ frame.status === "ddos" ? "DDoS" : "Normal" }}
					</td>
					<td class="px-6 py-4 whitespace-nowrap">
						<button
							type="button"
							class="text-blue-500 hover:underline focus:outline-none"
              title="View details"
              @click="showFrameDetails(frame)"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								fill="currentColor"
                class="w-4 h-4"
							>
								<path
									d="M18.031 16.6168L22.3137 20.8995L20.8995 22.3137L16.6168 18.031C15.0769 19.263 13.124 20 11 20C6.032 20 2 15.968 2 11C2 6.032 6.032 2 11 2C15.968 2 20 6.032 20 11C20 13.124 19.263 15.0769 18.031 16.6168ZM16.0247 15.8748C17.2475 14.6146 18 12.8956 18 11C18 7.1325 14.8675 4 11 4C7.1325 4 4 7.1325 4 11C4 14.8675 7.1325 18 11 18C12.8956 18 14.6146 17.2475 15.8748 16.0247L16.0247 15.8748ZM12.1779 7.17624C11.4834 7.48982 11 8.18846 11 9C11 10.1046 11.8954 11 13 11C13.8115 11 14.5102 10.5166 14.8238 9.82212C14.9383 10.1945 15 10.59 15 11C15 13.2091 13.2091 15 11 15C8.79086 15 7 13.2091 7 11C7 8.79086 8.79086 7 11 7C11.41 7 11.8055 7.06167 12.1779 7.17624Z"
								></path>
							</svg>
						</button>
					</td>
				</tr>
			</tbody>
		</table>
		<frameDetails
			:show="showDetails"
			:frame="frame"
			@hide="showDetails = false"
		/>
	</div>
	<div class="flex flex-col items-center justify-center w-full h-full text-center" v-else>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
			fill="currentColor"
			class="w-12 h-12 mb-4 text-gray-500"
		>
			<path
				d="M11 7H13V17H11V7ZM15 11H17V17H15V11ZM7 13H9V17H7V13ZM15 4H5V20H19V8H15V4ZM3 2.9918C3 2.44405 3.44749 2 3.9985 2H16L20.9997 7L21 20.9925C21 21.5489 20.5551 22 20.0066 22H3.9934C3.44476 22 3 21.5447 3 21.0082V2.9918Z"
			></path>
		</svg>
		<p class="font-semibold text-gray-500 mb-2">No results to display</p>
		<span class="text-gray-400">
			Please upload a pcap file and click the "Analyse" button
		</span>
	</div>
</template>

<script>
import FrameDetails from "./FrameDetails.vue";

export default {
	props: {
		frames: {
			type: Array,
			required: true,
		},
	},
	components: {
		FrameDetails,
	},
	data() {
		return {
			showDetails: false,
			frame: {},
		};
	},
  methods: {
    showFrameDetails(frame) {
      this.frame = frame;
      this.showDetails = true;
    },
  }
};
</script>
