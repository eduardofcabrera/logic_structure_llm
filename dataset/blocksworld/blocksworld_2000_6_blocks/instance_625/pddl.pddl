

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(ontable c)
(on d c)
(ontable e)
(clear a)
(clear b)
(clear d)
)
(:goal
(and
(on b e)
(on c d)
(on d b))
)
)


