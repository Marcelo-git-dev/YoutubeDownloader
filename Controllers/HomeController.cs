using Microsoft.AspNetCore.Mvc;  
using YoutubeDownloader.Models;  
using System.Threading.Tasks;  
using YoutubeExplode;  
using YoutubeExplode.Common;  
using System.IO;  
using System.Text.RegularExpressions;  

namespace YoutubeDownloader.Controllers  
{  
    public class HomeController : Controller  
    {  
        private readonly string _downloadsFolder = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "downloads");  

        public HomeController()  
        {  
            if (!Directory.Exists(_downloadsFolder))  
            {  
                Directory.CreateDirectory(_downloadsFolder);  
            }  
        }  

        public IActionResult Index()  
        {  
            return View(new DownloadModel());  
        }  

        [HttpPost]  
        public async Task<IActionResult> Download(DownloadModel model)  
        {  
            if (string.IsNullOrEmpty(model.Url))  
            {  
                ModelState.AddModelError("", "Por favor, insira uma URL válida.");  
                return View("Index", model);  
            }  

            string filePath = null;  
            try  
            {  
                var youtube = new YoutubeClient();  
                var videoId = YoutubeClient.ParseVideoId(model.Url);  
                var video = await youtube.Videos.GetAsync(videoId);  

                var streamManifest = await youtube.Videos.Streams.GetManifestAsync(videoId);  
                VideoStreamInfo streamInfo;  

                // Seleciona o melhor formato disponível  
                if (model.Format == "best")  
                {  
                    streamInfo = streamManifest.GetMuxedStreams().GetMuxedStreamByType(MediaStreamType.Audio | MediaStreamType.Video);  
                }  
                else  
                {  
                    streamInfo = streamManifest.GetMuxedStreams().GetMuxedStreamByType(MediaStreamType.Audio | MediaStreamType.Video);  
                }  

                var stream = await youtube.Videos.Streams.GetAsync(streamInfo);  
                filePath = Path.Combine(_downloadsFolder, $"{SanitizeFileName(video.Title)}.{streamInfo.Container}");  

                using (var fileStream = new FileStream(filePath, FileMode.Create, FileAccess.Write, FileShare.None))  
                {  
                    await stream.CopyToAsync(fileStream);  
                }  

                ViewBag.SuccessMessage = "Download concluído com sucesso!";  
                ViewBag.DownloadPath = $"/downloads/{Path.GetFileName(filePath)}";  
            }  
            catch (Exception ex)  
            {  
                ModelState.AddModelError("", $"Erro ao baixar o vídeo: {ex.Message}");  
                return View("Index", model);  
            }  

            return View("Index", model);  
        }  

        private string SanitizeFileName(string fileName)  
        {  
            // Remove caracteres inválidos do nome do arquivo  
            return Regex.Replace(fileName, @"[<>:""/\\|?*\x00-\x1F]", "_");  
        }  
    }  
}  