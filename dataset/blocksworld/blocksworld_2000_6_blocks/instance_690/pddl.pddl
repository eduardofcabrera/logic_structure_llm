

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c a)
(on d c)
(on e d)
(clear b)
)
(:goal
(and
(on a b)
(on b e)
(on c d))
)
)


