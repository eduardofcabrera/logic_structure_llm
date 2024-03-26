

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b a)
(on c b)
(on d e)
(ontable e)
(clear c)
)
(:goal
(and
(on a d)
(on c e)
(on d c))
)
)


