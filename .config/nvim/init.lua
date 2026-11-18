vim.lsp.enable("pyright")

-- local set = vim.api.nvim.set_keymap
-- local ns = { noremap = true, silent = true }


vim.g.mapleader = " "
vim.keymap.set("i", "ii", "<Esc>")

vim.api.nvim_create_autocmd("LspAttach", {
    callback = function(args)
        local opts = { buffer = args.buf }
        vim.keymap.set("n", "K", vim.lsp.buf.hover, opts)
        vim.keymap.set("n", "gd", vim.lsp.buf.definition, opts)
        vim.keymap.set("n", "gr", vim.lsp.buf.references, opts)
        vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts)
        vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action, opts)
    end,
})

vim.diagnostic.config({
    virtual_text = true,
})
