

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c d)
(on d e)
(ontable e)
(clear a)
(clear b)
(clear c)
)
(:goal
(and
(on d b)
(on e d))
)
)


