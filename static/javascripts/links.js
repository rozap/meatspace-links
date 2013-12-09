$(document).ready(function() {
	/*
		Music controller ==========================================
	*/

	var Controller = function() {
		this.WHAT = "OIHSAF"


		var $ytPlayer = $('#yt-player');
		var $scPlayer = $('#sc-player');

		//Bind to stuff
		var that = this;
		$('.music-control').on('click', function(e) {
			var $t = $(e.currentTarget);
			var action = $t.data('action');
			if (that[action]) {
				that[action].call(that, e, $t);
			}
		});


		//some vars wow
		var linkList = [],
			currentLinkIndex = -1;


		/*
			Adapters ================================================
		*/
		this.linkAdapters = {
			'www.youtube.com': function(link, pathname, query) {
				$ytPlayer.show();
				$scPlayer.hide();
				var match = /\?v=(.+)/.exec(query);
				var key = match && match[1];

				if (!key) return;
				this.youtubePlayer.loadVideoById({
					videoId: key
				});
			},

			'soundcloud.com': function(link, pathname, query) {
				var that = this;
				$ytPlayer.hide();
				$scPlayer.show();
				SC.oEmbed(link, {
					auto_play: true,
					enable_api: true,
				}, $scPlayer[0], function() {
					that.scWidget = SC.Widget($scPlayer.find('iframe')[0]);
					that.scWidget.bind(SC.Widget.Events.FINISH, function() {
						that.playNext();
					});
				});

			}

		};

		this.adaptLink = function(link) {
			a = document.createElement('a');
			a.href = link;
			var adapter = this.linkAdapters[a.host];
			if (adapter) {
				adapter.call(this, link, a.pathname, a.search)
			} else {
				console.warn("No adapter for ", link, a.host);
			}
		}

		this.stopAllMusic = function() {
			if (this.youtubePlayer) {
				this.youtubePlayer.stopVideo();
			}
			//ugh...no stop function?
			$scPlayer.children().detach();

		}


		/*
			Get a random song from the server and queue it up
		*/
		this.getRandomMusic = function() {
			this.stopAllMusic();
			var that = this;
			$.getJSON('/api/music/random', function(r) {
				linkList.push(r.link);
				currentLinkIndex++;
				that.adaptLink(r.link)
			});
		}


		this.playNext = function() {
			if (currentLinkIndex === linkList.length - 1) {
				this.getRandomMusic();
			} else {
				currentLinkIndex++;
				adaptLink(linkList[currentLinkIndex]);
			}
		}


		this.next = function(e, $target) {
			this.playNext();
		};

		this.previous = function(e, $target) {
			if (currentLinkIndex > 0) {
				currentLinkIndex--;
				adaptLink(linkList[currentLinkIndex]);
			}
		};


		this.show = function() {
			$('.music-player').show();
			$('.music-start').hide();
			this.getRandomMusic();
		};
	};

	var controller = new Controller();



	//debug
	window.controller = controller;

	/*
		YouTube crap =======================================
	*/
	window.onYouTubeIframeAPIReady = function() {
		controller.youtubePlayer = new YT.Player('yt-player-el', {
			height: '220',
			width: '320',
			events: {
				'onReady': onPlayerReady,
				'onStateChange': onPlayerStateChange
			}
		});

	}

	window.onPlayerReady = function(event) {

	};

	window.onPlayerStateChange = function(event) {
		//pretty cool how these are just magic numbers
		if (event.data == 0) {
			controller.playNext();
		}
	}
});